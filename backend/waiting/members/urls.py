from django.urls import path

from . import views


urlpatterns = [
    path('', views.MembersEndpoint.as_view()),
    path('/<str:id>', views.MembersEndpoint.as_view()),
]
