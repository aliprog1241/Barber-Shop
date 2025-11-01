from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('api/services/', include('services.urls')),
    path('api/staff/', include('staff.urls')),
    path('api/booking/', include('booking.urls')),
]

# برای سرو تصاویر آواتار در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
