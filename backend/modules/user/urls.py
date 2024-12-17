from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('me', views.Me.as_view(), name='me'),
]
