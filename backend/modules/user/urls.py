from django.urls import path

from . import views

urlpatterns = [
    path('', views.GetMe.as_view(), name='me'),
]
