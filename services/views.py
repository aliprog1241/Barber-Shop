from django.http import JsonResponse
from .models import Service

def service_list(request):
    qs = Service.objects.filter(is_active=True).values(
        "id", "title", "duration_minutes", "price"
    )
    return JsonResponse(list(qs), safe=False)
