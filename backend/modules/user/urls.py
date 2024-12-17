from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('me', views.Me.as_view(), name='me'),
    path('user', views.CreateUser.as_view(), name='create_user')
]
