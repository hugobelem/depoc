from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('modules.accounts.urls')),
    path('business', include('modules.business.urls')),
    path('contacts', include('modules.contacts.urls')),
    path('finance', include('modules.finance.urls')),
    path('members', include('modules.members.urls')),
    path('products', include('modules.inventory.urls')),
    path('products', include('modules.products.urls')),
    path('', include('modules.billing.urls')),

    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
