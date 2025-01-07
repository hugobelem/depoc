from django.urls import path

from . import views


urlpatterns = [
    path('/inventory', views.InventoryEndpoint.as_view()),
    path('/<str:product_id>/inventory', views.InventoryEndpoint.as_view()),
]
