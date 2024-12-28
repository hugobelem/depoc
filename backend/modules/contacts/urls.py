from django.urls import path

from . import views


urlpatterns = [
    path('', views.ContactsEndpoint.as_view()),
    path('/<str:id>', views.ContactsEndpoint.as_view()),
]
