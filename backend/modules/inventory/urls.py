from django.urls import path

from . import views


urlpatterns = [
    path('/inventory', views.InventoryEndpoint.as_view()),
    path('/inventory/<str:inventory_id>', views.InventoryEndpoint.as_view()),

    path(
        '/inventory/<str:inventory_id>/transactions',
        views.InventoryTransactionEndpoint.as_view(),
    ),
    path(
        '/inventory/transactions/<str:transaction_id>',
        views.InventoryTransactionEndpoint.as_view(),
    ),
]
