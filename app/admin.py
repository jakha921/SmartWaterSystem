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
    list_filter = ['city__name_ru']


admin.site.register(models.User, CustomUserAdmin)


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_ru', 'name_uz', 'name_en', 'created_at', 'updated_at']
    list_display_links = ['name_ru']
    list_per_page = 10
    search_fields = ['name_ru', 'name_uz', 'name_en']

    # required fields for add new object
    fields = ['name_ru', 'name_uz', 'name_en']

    # readonly fields for update object
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_ru', 'name_uz', 'name_en', 'city', 'created_at', 'updated_at']
    list_display_links = ['name_ru']
    list_filter = ['city__name_ru']
    list_per_page = 20
    search_fields = ['name_ru', 'name_uz', 'name_en']

    # required fields for add new object
    fields = ['name_ru', 'name_uz', 'name_en', 'city']

    # readonly fields for update object
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.DeviceInfo)
class DeviceInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'object_name', 'district', 'sim', 'latitude', 'longitude', 'IMEI']
    list_display_links = ['code']
    list_filter = ['district__city__name_ru', 'district__name_ru']
    list_per_page = 20
    search_fields = ['code', 'object_name', 'organization', 'latitude', 'longitude', 'sim', 'verified_at',
                     'IMEI', 'modem_number', 'device_number', 'district__name_ru']

    # # required fields for add new object
    fields = ['code', 'object_name', 'district', 'organization', ('latitude', 'longitude'), 'sim', 'verified_at',
              'IMEI', 'modem_number', 'device_number']
    list_editable = ['object_name', 'district']

    # readonly fields for update object
    readonly_fields = ['created_at', 'updated_at']
    actions = ['download_csv']

    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

        writer = csv.writer(response)
        # writer.writerow(['Name', 'Date', 'Time', 'Device ID'])
        writer.writerow(['№', 'code', 'object_name', 'district',
                         'modem_number', 'device_number'])

        for index, item in enumerate(queryset):
            # change date format to 'DD-MM-YYYY'
            # writer.writerow([index + 1, item.name, item.date.strftime('%d-%m-%Y'), item.time])
            writer.writerow([index + 1, item.code, item.object_name, item.district,
                             item.modem_number, item.device_number])

        return response

    download_csv.short_description = 'CSV fayl qilib yuklash'


@admin.register(models.Consumption)
class ConsumptionAdmin(admin.ModelAdmin):
    # order by device_update_at desc
    ordering = ['-device_update_at']
    list_display = ['device_info', 'average_volume', 'volume', 'device_update_at']
    list_filter = ['device_info__district__city__name_ru', 'device_info__district__name_ru']
    list_per_page = 20
    search_fields = ['device_info__code', 'average_volume', 'volume', 'device_info__district__name_ru',
                     'device_info__district__city__name_ru']

    # required fields for add new object
    fields = ['device_info', 'average_volume', 'volume', 'device_update_at']
