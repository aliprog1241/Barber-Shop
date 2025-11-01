# models.py
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام سرویس')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='قیمت')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال؟')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'سرویس'
        verbose_name_plural = 'سرویس‌ها'

    def __str__(self):
        return self.name
