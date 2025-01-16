from django.urls import path

from . import views


urlpatterns = [
    path(
        '/accounts',
        views.FinancialAccountEndpoint.as_view()
    ),
    path(
        '/accounts/<str:account_id>',
        views.FinancialAccountEndpoint.as_view()
    ),
    path(
        '/categories',
        views.FinancialCategoryEndpoint.as_view()
    ),
    path(
        '/categories/<str:category_id>',
        views.FinancialCategoryEndpoint.as_view()
    ),
    path(
        '/transactions',
         views.FinancialTransactionEndpoint.as_view()
    ),
    path(
        '/transactions/<str:transaction_id>',
        views.FinancialTransactionEndpoint.as_view()
    ),
]
