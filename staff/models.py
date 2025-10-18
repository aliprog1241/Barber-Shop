from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)  # آرایشگر، ناخن‌کار، کلرینگ…
    bio  = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/', blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)  # ["شینیون","کاشت","رنگ","کوتاهی"]
    is_active = models.BooleanField(default=True)

    def __str__(self): return self.name
