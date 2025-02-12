from django.urls import path

from . import views


urlpatterns = [
    path('receivables', views.ReceivablesEndpoint.as_view()),
    path('receivables/', views.ReceivableSearchEndpoint.as_view()),
    path('receivables/<str:receivable_id>', views.ReceivablesEndpoint.as_view()),
    path(
        'receivables/<str:receivable_id>/settle',
        views.ReceivableSettleEndpoint.as_view()
    ),
    path('payables', views.PayablesEndpoint.as_view()),
    path('payables/', views.PayableSearchEndpoint.as_view()),
    path('payables/<str:payable_id>', views.PayablesEndpoint.as_view()),
    path(
        'payables/<str:payable_id>/settle',
        views.PayableSettleEndpoint.as_view()
    ),
]
