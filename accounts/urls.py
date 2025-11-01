from django.urls import path

from accounts.views import HomePageView

urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
]
