from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('', views.CreateMerchant.as_view()),
    path('/me', views.Merchant.as_view()),
]
