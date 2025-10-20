from django.http import JsonResponse
from .models import Staff

def staff_list(request):
    data = []
    for s in Staff.objects.filter(is_active=True).prefetch_related("services"):
        data.append({
            "id": s.id,
            "name": s.name,
            "bio": s.bio,
            "avatar": s.avatar.url if s.avatar else None,
            "services": [{"id": sv.id, "title": sv.title} for sv in s.services.all()],
        })
    return JsonResponse(data, safe=False)
