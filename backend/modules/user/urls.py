from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('me', views.MeEndpoint.as_view()),
    path('owner', views.OwnerEndpoint.as_view()),
]
