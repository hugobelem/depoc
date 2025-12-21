from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from .settings import ENVIRONMENT

secure = True
if ENVIRONMENT == 'development':
    secure = False

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            "access": access_token,
            "refresh": refresh_token
        })
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=secure,
            samesite='Lax',
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='Lax',
        )

        return response

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

    path('token', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
