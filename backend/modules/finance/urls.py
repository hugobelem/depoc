from django.urls import path

from . import views


urlpatterns = [
    path('', views.BankAccountEndpoint.as_view()),
]
