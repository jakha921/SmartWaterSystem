from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # JWT verify token
]
