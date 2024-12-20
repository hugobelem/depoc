from django.urls import path

from . import views


urlpatterns = [
    path('', views.BusinessEndpoint.as_view()),
]
