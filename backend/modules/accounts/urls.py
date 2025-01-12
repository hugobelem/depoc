from django.urls import path

from . import views


urlpatterns = [
    path('me', views.MeEndpoint.as_view()),
    path('accounts', views.AccountsEndpoint.as_view()),
    path('owner', views.OwnerEndpoint.as_view()),
]
