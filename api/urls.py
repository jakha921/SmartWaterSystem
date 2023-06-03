from django.urls import include, path, re_path
from rest_framework import routers

from api import views
from api.swagger import urlpatterns as swagger_urlpatterns
from api.jwt import urlpatterns as jwt_urlpatterns

router = routers.DefaultRouter()
router.register(r'consumptions', views.ConsumptionViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('consumptions/', views.ConsumptionViewSet.as_view({'get': 'list'}), name='consumptions'),
    path('consumption/<str:start_date_time>/<str:end_date_time>/<int:device_id>/',
         views.ConsumptionViewSet.as_view({'get': 'list'}), name='consumption-filtered'),
    path('devices/', views.DeviceInfoViewSet.as_view({'get': 'list'}), name='devices-list'),
    path('cities/', views.CityViewSet.as_view({'get': 'list'}), name='cities-list'),
    path('user/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('user/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='user-detail'),
]

urlpatterns += swagger_urlpatterns
urlpatterns += jwt_urlpatterns
