from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Smart Water API",
        default_version='',
        description="Smart Water API description",
        contact=openapi.Contact(name='Jakha921'),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    # path('docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # download documentation in some format
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # documentation
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # another documentation
]
