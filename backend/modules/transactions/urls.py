from django.urls import path

from . import views


urlpatterns = [
    path('', views.TransactionEndpoint.as_view()),
    path('/<str:id>', views.TransactionEndpoint.as_view()),
]
