from django.urls import path

from . import views


urlpatterns = [
    path('/inventory', views.InventoryEndpoint.as_view()),
    path('/<str:product_id>/inventory', views.InventoryEndpoint.as_view()),

    path(
        '/<str:product_id>/inventory/transactions',
        views.InventoryTransactionEndpoint.as_view(),
    ),
    path(
        '/<str:product_id>/inventory/transactions/<str:transaction_id>',
        views.InventoryTransactionEndpoint.as_view(),
    ),
]
