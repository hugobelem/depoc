from django.urls import path

from . import views


urlpatterns = [
    path('/categories', views.ProductCategoryEndpoint.as_view()),
    path('/categories/<str:id>', views.ProductCategoryEndpoint.as_view()),
    path(
        '/<str:product_id>/costs',
        views.ProductCostHistoryEndpoint.as_view()
    ),
    path(
        '/<str:product_id>/costs/<str:cost_id>',
        views.ProductCostHistoryEndpoint.as_view()
    ),
    path('', views.ProductsEndpoint.as_view()),
    path('/<str:id>', views.ProductsEndpoint.as_view()),
]
