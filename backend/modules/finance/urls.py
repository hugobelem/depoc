from django.urls import path

from . import views


urlpatterns = [
    path('/categories', views.CategoryEndpoint.as_view()),
    path('/categories/<str:id>', views.CategoryEndpoint.as_view()),
    path('', views.BankAccountEndpoint.as_view()),
    path('/<str:id>', views.BankAccountEndpoint.as_view()),
]
