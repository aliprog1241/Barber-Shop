class Service(models.Model):
    name = models.CharField(max_length=120)      # شینیون، کاشت ناخن، رنگ، کوتاهی...
    duration_min = models.PositiveIntegerField() # مدت زمان سرویس
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self): return self.name
