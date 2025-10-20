import json
from datetime import datetime, timedelta, time
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from django.core.mail import send_mail
from django.conf import settings

from .models import Booking, WorkingHour
from services.models import Service
from staff.models import Staff

@require_GET
def booking_list(request):
    qs = Booking.objects.select_related("service", "staff").order_by("-date", "-start_time")[:100]
    payload = []
    for b in qs:
        payload.append({
            "id": b.id,
            "customer_name": b.customer_name,
            "customer_phone": b.customer_phone,
            "service": {"id": b.service_id, "title": b.service.title, "duration": b.service.duration_minutes},
            "staff": {"id": b.staff_id, "name": b.staff.name},
            "date": b.date.isoformat(),
            "start_time": b.start_time.strftime("%H:%M"),
            "end_time": b.end_time.strftime("%H:%M"),
            "is_confirmed": b.is_confirmed,
        })
    return JsonResponse(payload, safe=False)


@require_GET
def available_slots(request):
    """
    ورودی‌های لازم: ?staff_id=&service_id=&date=YYYY-MM-DD&step=15
    خروجی: لیست تایم‌های آزاد
    """
    try:
        staff_id = int(request.GET.get("staff_id"))
        service_id = int(request.GET.get("service_id"))
        date_str = request.GET.get("date")
        step = int(request.GET.get("step", 15))  # فاصله‌ی تست اسلات‌ها
    except (TypeError, ValueError):
        return HttpResponseBadRequest("پارامترها نامعتبرند.")

    try:
        staff = Staff.objects.get(pk=staff_id, is_active=True)
        service = Service.objects.get(pk=service_id, is_active=True)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (Staff.DoesNotExist, Service.DoesNotExist, ValueError):
        return HttpResponseBadRequest("داده‌ها یافت نشد یا تاریخ نامعتبر است.")

    try:
        wh = staff.working_hours.get(weekday=date_obj.weekday())
    except WorkingHour.DoesNotExist:
        return JsonResponse({"slots": []})

    # اسلات‌ها را در بازه‌ی کاری بساز
    def to_dt(t: time): return datetime.combine(date_obj, t)
    start_dt, end_dt = to_dt(wh.start_time), to_dt(wh.end_time)
    duration = timedelta(minutes=service.duration_minutes)
    step_delta = timedelta(minutes=step)

    # رزروهای روز
    todays = list(Booking.objects.filter(staff=staff, date=date_obj))
    slots = []
    cur = start_dt
    while cur + duration <= end_dt:
        cur_end = cur + duration
        # تداخل با رزروهای موجود
        has_overlap = any((cur.time() < b.end_time) and (cur_end.time() > b.start_time) for b in todays)
        if not has_overlap:
            slots.append({"start": cur.strftime("%H:%M"), "end": cur_end.strftime("%H:%M")})
        cur += step_delta

    return JsonResponse({"slots": slots})


@require_POST
def create_booking(request):
    """
    JSON body:
    {
      "customer_name": "...",
      "customer_phone": "...",
      "customer_email": "optional",
      "service_id": 1,
      "staff_id": 1,
      "date": "2025-10-20",
      "start_time": "14:30"
    }
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
        service = Service.objects.get(pk=int(data["service_id"]))
        staff = Staff.objects.get(pk=int(data["staff_id"]))
        date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(data["start_time"], "%H:%M").time()
    except Exception as e:
        return HttpResponseBadRequest(f"خطا در داده‌های ورودی: {e}")

    booking = Booking(
        customer_name=data.get("customer_name", "").strip(),
        customer_phone=data.get("customer_phone", "").strip(),
        customer_email=data.get("customer_email"),
        service=service,
        staff=staff,
        date=date_obj,
        start_time=start_time_obj,
    )

    try:
        booking.save()
    except Exception as e:
        return HttpResponseBadRequest(str(e))

    # ایمیل تأیید (اختیاری؛ اگر SMTP ست شده باشد)
    if getattr(settings, "EMAIL_HOST", None) and booking.customer_email:
        try:
            send_mail(
                subject="تأیید رزرو شما",
                message=f"رزرو شما برای {service.title} در {booking.date} ساعت {booking.start_time} ثبت شد.",
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                recipient_list=[booking.customer_email],
                fail_silently=True,
            )
        except Exception:
            pass

    return JsonResponse({
        "id": booking.id,
        "message": "رزرو با موفقیت ثبت شد.",
        "start_time": booking.start_time.strftime("%H:%M"),
        "end_time": booking.end_time.strftime("%H:%M"),
    }, status=201)
