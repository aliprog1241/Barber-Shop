from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

DAYS_OF_WEEK = (
    (0, "Monday"), (1, "Tuesday"), (2, "Wednesday"),
    (3, "Thursday"), (4, "Friday"), (5, "Saturday"), (6, "Sunday"),
)

class WorkingHour(models.Model):
    staff = models.ForeignKey("staff.Staff", on_delete=models.CASCADE, related_name="working_hours")
    weekday = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()  # مثلا 10:00
    end_time = models.TimeField()    # مثلا 19:00

    class Meta:
        unique_together = ("staff", "weekday")
        ordering = ["staff", "weekday"]

    def __str__(self):
        return f"{self.staff} - {self.get_weekday_display()} {self.start_time}–{self.end_time}"


class Booking(models.Model):
    customer_name = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=32)
    customer_email = models.EmailField(blank=True, null=True)

    service = models.ForeignKey("services.Service", on_delete=models.PROTECT, related_name="bookings")
    staff = models.ForeignKey("staff.Staff", on_delete=models.PROTECT, related_name="bookings")

    date = models.DateField()
    start_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date", "-start_time"]

    def __str__(self):
        return f"{self.customer_name} - {self.service} - {self.date} {self.start_time}"

    @property
    def end_time(self):
        # محاسبه‌ی پایان با توجه به مدت سرویس
        start_dt = datetime.combine(self.date, self.start_time)
        end_dt = start_dt + timedelta(minutes=self.service.duration_minutes)
        return end_dt.time()

    def clean(self):
        # 1) بررسی این‌که استایلست این سرویس را ارائه می‌دهد
        if not self.staff.services.filter(pk=self.service_id).exists():
            raise ValidationError("این نیروی کار این سرویس را ارائه نمی‌دهد.")

        # 2) داخل بازه‌ی کاری آن روز باشد
        weekday = self.date.weekday()
        try:
            wh = self.staff.working_hours.get(weekday=weekday)
        except WorkingHour.DoesNotExist:
            raise ValidationError("برای این روز ساعت کاری ثبت نشده است.")

        if not (wh.start_time <= self.start_time < wh.end_time):
            raise ValidationError("شروع رزرو خارج از ساعت کاری است.")

        if not (wh.start_time < self.end_time <= wh.end_time):
            raise ValidationError("پایان رزرو خارج از ساعت کاری است.")

        # 3) تداخل نداشتن با رزروهای دیگر
        overlaps = Booking.objects.filter(
            staff=self.staff, date=self.date
        ).exclude(pk=self.pk)

        for b in overlaps:
            # اگر بازه‌ها هم‌پوشانی داشته باشند خطا بده
            if (self.start_time < b.end_time) and (self.end_time > b.start_time):
                raise ValidationError("زمان انتخابی با رزرو دیگری تداخل دارد.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
