from django.db import models
from django.utils import timezone
from staff.models import Staff
from services.models import Service

class WorkingHour(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    weekday = models.PositiveSmallIntegerField()  # 0=دوشنبه؟ (پایه را یکسان تعیین می‌کنیم)
    start = models.TimeField()
    end   = models.TimeField()

class Booking(models.Model):
    PENDING, CONFIRMED, CANCELED, DONE = "P","C","X","D"
    STATUS_CHOICES = [(PENDING,"در انتظار"),(CONFIRMED,"تأیید"),(CANCELED,"لغو"),(DONE,"انجام‌شده")]

    customer_name  = models.CharField(max_length=120)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    staff   = models.ForeignKey(Staff, on_delete=models.PROTECT)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    start_at = models.DateTimeField()
    end_at   = models.DateTimeField()
    note     = models.TextField(blank=True)
    status   = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-start_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["staff","start_at","end_at"], name="unique_staff_timeslot"
            )
        ]
