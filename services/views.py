# services/views.py
from django.http import JsonResponse

def service_list(request):
    data = [
        {"id": 1, "title": "کوتاهی مو", "price": 300_000, "duration": 45},
        {"id": 2, "title": "رنگ مو",   "price": 900_000, "duration": 120},
        {"id": 3, "title": "شنیون",    "price": 700_000, "duration": 90},
    ]
    return JsonResponse(data, safe=False)
