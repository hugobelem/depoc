from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductsEndpoint.as_view()),
    path('/<str:id>', views.ProductsEndpoint.as_view()) 
]
