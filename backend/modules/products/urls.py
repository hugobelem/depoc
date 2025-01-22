from django.urls import path

from . import views


urlpatterns = [
    path('/categories', views.ProductCategoryEndpoint.as_view()),
    path('/categories/<str:category_id>', views.ProductCategoryEndpoint.as_view()),

    path('/<str:product_id>/costs',
         views.ProductCostHistoryEndpoint.as_view(),
        ),
    path(
        '/<str:product_id>/costs/<str:cost_id>',
        views.ProductCostHistoryEndpoint.as_view(),
    ),

    path('/', views.ProductSearchEndpoint.as_view()),
    
    path('', views.ProductEndpoint.as_view()),
    path('/<str:product_id>', views.ProductEndpoint.as_view()),
]
