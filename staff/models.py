from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=120)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="staff/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # مهارت‌ها: به چه سرویس‌هایی می‌تونه خدمت بده
    services = models.ManyToManyField("services.Service", related_name="staff_members", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
