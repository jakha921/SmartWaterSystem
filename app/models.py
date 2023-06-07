from importlib.resources import _

from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.urls import reverse


# Create your models here.
class City(models.Model):
    name_ru = models.CharField(max_length=255)
    name_uz = models.CharField(max_length=255, null=True)
    name_en = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_ru

    class Meta:
        db_table = 'cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name_ru']


class District(models.Model):
    name_ru = models.CharField(max_length=255)
    name_uz = models.CharField(max_length=255, null=True)
    name_en = models.CharField(max_length=255, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.city.name_ru} - {self.name_ru}'

    class Meta:
        db_table = 'districts'
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'
        ordering = ['name_ru']


#
class User(AbstractUser):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)


class DeviceInfo(models.Model):
    code = models.CharField(max_length=255, null=False)
    object_name = models.CharField(max_length=255, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    organization = models.CharField(max_length=255, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    sim = models.CharField(max_length=255, null=True)
    verified_at = models.DateTimeField(null=True)
    IMEI = models.CharField(max_length=255, null=True)
    modem_number = models.CharField(max_length=255, null=True)
    device_number = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.district}"

    def get_absolute_url(self):
        return reverse('device_info_detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'device_infos'
        verbose_name = 'Информация об устройстве'
        verbose_name_plural = 'Информация об устройствах'
        ordering = ['code']


class Consumption(models.Model):
    device_info = models.ForeignKey(DeviceInfo, on_delete=models.CASCADE)
    average_volume = models.FloatField(null=False)
    volume = models.FloatField(null=False)
    device_update_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_info.code} - {self.volume} at {self.device_update_at}"

    class Meta:
        db_table = 'consumptions'
        verbose_name = 'Потребление'
        verbose_name_plural = 'Потребления'
        ordering = ['updated_at']
