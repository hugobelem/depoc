from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('', views.Me.as_view(), name='me'),
]
