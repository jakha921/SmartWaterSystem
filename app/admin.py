from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = models.User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('city',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('city',)}),
    )


admin.site.register(models.User, CustomUserAdmin)


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name_uz', 'name_en', 'created_at', 'updated_at']
    list_filter = ['name_ru']
    list_per_page = 10
    search_fields = ['name_ru', 'name_uz', 'name_en']

    # required fields for add new object
    fields = ['name_ru', 'name_uz', 'name_en']

    # readonly fields for update object
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name_ru', 'name_uz', 'name_en', 'city', 'created_at', 'updated_at']
    list_filter = ['name_ru']
    list_per_page = 20
    search_fields = ['name_ru', 'name_uz', 'name_en']

    # required fields for add new object
    fields = ['name_ru', 'name_uz', 'name_en', 'city']

    # readonly fields for update object
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.DeviceInfo)
class DeviceInfoAdmin(admin.ModelAdmin):
    list_display = ['code', 'object_name', 'district', 'sim', 'latitude', 'longitude', 'IMEI']
    list_filter = ['code']
    list_per_page = 20
    search_fields = ['code', 'object_name', 'organization', 'latitude', 'longitude', 'sim', 'verified_at',
                     'IMEI', 'modem_number', 'device_number', 'district__name_ru']

    # # required fields for add new object
    fields = ['code', 'object_name', 'district', 'organization', ('latitude', 'longitude'), 'sim', 'verified_at',
              'IMEI', 'modem_number', 'device_number']

    # readonly fields for update object
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    # order by device_update_at desc
    ordering = ['-device_update_at']
    list_display = ['device_info', 'average_volume', 'volume', 'device_update_at']
    list_filter = ['device_info']
    list_per_page = 20
    search_fields = ['device_info__code', 'average_volume', 'volume', 'device_info__district__name_ru',
                     'device_info__district__city__name_ru']

    # required fields for add new object
    fields = ['device_info', 'average_volume', 'volume', 'device_update_at']
