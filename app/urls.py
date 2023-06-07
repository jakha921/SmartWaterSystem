from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import views

app_name = 'app'  # Замените 'app' на имя вашего основного приложения

urlpatterns = [
    path('', views.write_db, name='write_db'),
    path('main/', views.main, name='main'),
    path('index/', views.index, name='index'),
    path('tables/', views.TablesView.as_view(), name='tables'),
    path('devices/', views.DevicesView.as_view(), name='devices'),
    path('devices/<int:pk>/edit/', views.DevicesView.as_view(), name='device_edit'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('error/', views.error, name='error'),
    path('pagination/', views.pagination, name='pagination'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
