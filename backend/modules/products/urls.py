from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProductsEndpoint.as_view())    
]
