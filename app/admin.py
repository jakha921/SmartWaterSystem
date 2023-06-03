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
    list_per_page = 10
    search_fields = ['name_ru', 'name_uz', 'name_en']

    # required fields for add new object
    fields = ['name_ru', 'name_uz', 'name_en', 'city']

    # readonly fields for update object
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.DeviceInfo)
class DeviceInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    list_display = ['device_info', 'average_volume', 'volume', 'device_update_at']
    list_filter = ['device_info']
    list_per_page = 10
    search_fields = ['device_info', 'average_volume', 'volume']

    # required fields for add new object
    fields = ['device_info', 'average_volume', 'volume', 'device_update_at']
