from django.conf.urls.static import static
from django.urls import path

from config import settings
from . import views

urlpatterns = [
    path('', views.write_db, name='write_db'),
    path('main', views.main, name='main'),
    path('index/', views.index, name='index'),
    # path('login/', views.login, name='login'),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('tables/', views.TablesView.as_view(), name='tables'),
    path('devices/', views.DevicesView.as_view(), name='devices'),
    path('devices/<int:pk>/edit/', views.DevicesView.as_view(), name='device_edit'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('error/', views.error, name='error'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)