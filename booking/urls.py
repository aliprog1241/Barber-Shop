from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('available-slots/', views.available_slots, name='available_slots'),
    path('create/', views.create_booking, name='create_booking'),
]
