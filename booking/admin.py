from django.contrib import admin
from .models import Booking, WorkingHour

@admin.register(WorkingHour)
class WorkingHourAdmin(admin.ModelAdmin):
    list_display = ("staff", "weekday", "start_time", "end_time")
    list_filter = ("weekday", "staff")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "service", "staff", "date", "start_time", "is_confirmed")
    list_filter = ("date", "staff", "service", "is_confirmed")
    search_fields = ("customer_name", "customer_phone", "customer_email")
