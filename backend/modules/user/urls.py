from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('me', views.GetMe.as_view()),
    path('owner', views.Owner.as_view()),
]
