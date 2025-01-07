from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('modules.user.urls')),
    path('business', include('modules.business.urls')),
    path('members', include('modules.members.urls')),
    path('contacts', include('modules.contacts.urls')),
    path('products', include('modules.inventory.urls')),
    path('products', include('modules.products.urls')),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
