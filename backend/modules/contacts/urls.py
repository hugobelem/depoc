from django.urls import path

from . import views


urlpatterns = [
    path('', views.ContactsEndpoint.as_view()),
    path('/', views.ContactsSearchEndpoint.as_view()),
    path('/customers', views.CustomerEndpoint.as_view()),
    path('/customers/<str:customer_id>', views.CustomerEndpoint.as_view()),
    path('/suppliers', views.SupplierEndpoint.as_view()),
    path('/suppliers/<str:supplier_id>', views.SupplierEndpoint.as_view()),
]
