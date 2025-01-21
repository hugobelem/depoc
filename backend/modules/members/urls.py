from django.urls import path

from . import views


urlpatterns = [
    path('', views.MemberEndpoint.as_view()),
    path('/<str:member_id>', views.MemberEndpoint.as_view()),
]
