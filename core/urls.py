from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # صفحه اصلی (همون index.html)
    path('', TemplateView.as_view(template_name="index.html"), name='home'),

    # API های ما
    path('api/services/', include('services.urls')),
    path('api/staff/', include('staff.urls')),
    path('api/booking/', include('booking.urls')),
]

