from django.contrib.auth.models import User, Group
from rest_framework import serializers

from app.models import Consumption, DeviceInfo, City, District


class ConsumptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Consumption model from app.models

    {
        "id": 1,
        "device": {
            "id": 1,
            "code": "xdnrzo6ie",
            "latitude": 43.238949,
            "longitude": 76.889709,
            "sim": "87477222222",
            "district": {
                "id": 1,
                "name_ru": "Алатауский район",
                "name_uz": "Алатауский район",
                "name_en": "Alatau district",
                "city": {
                    "id": 1,
                    "name_ru": "Алматы",
                    "name_uz": "Алматы",
                    "name_en": "Almaty"
                }
            },
        },
        }
        "average_volume": 100.0,
        "volume": 100.0,
        "updated_at": "2020-07-07T12:00:00Z"

    }
    """
    device = serializers.SerializerMethodField()

    def get_device(self, obj):
        return {
            "id": obj.device_info.id,
            "code": obj.device_info.code,
            "latitude": obj.device_info.latitude,
            "longitude": obj.device_info.longitude,
            "sim": obj.device_info.sim,
            "district": {
                "id": obj.device_info.district.id,
                "name_ru": obj.device_info.district.name_ru,
                "name_uz": obj.device_info.district.name_uz,
                "name_en": obj.device_info.district.name_en,
                "city": {
                    "id": obj.device_info.district.city.id,
                    "name_ru": obj.device_info.district.city.name_ru,
                    "name_uz": obj.device_info.district.city.name_uz,
                    "name_en": obj.device_info.district.city.name_en,
                }
            },
        }

    class Meta:
        model = Consumption
        fields = ['id', 'device', 'average_volume', 'volume', 'updated_at']


class DeviceInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for DeviceInfo model from app.models

    {
        "id": 1,
        "code": "xdnrzo6ie",
        "latitude": 43.238949,
        "longitude": 76.889709,
        "sim": "87477222222",
        "district": {
            "id": 1,
            "name_ru": "Алатауский район",
            "name_uz": "Алатауский район",
            "name_en": "Alatau district",
            "city": {
                "id": 1,
                "name_ru": "Алматы",
                "name_uz": "Алматы",
                "name_en": "Almaty"
            }
        },
    }
    """
    district = serializers.SerializerMethodField()

    def get_district(self, obj):
        return {
            "id": obj.district.id,
            "name_ru": obj.district.name_ru,
            "name_uz": obj.district.name_uz,
            "name_en": obj.district.name_en,
            "city": {
                "id": obj.district.city.id,
                "name_ru": obj.district.city.name_ru,
                "name_uz": obj.district.city.name_uz,
                "name_en": obj.district.city.name_en,
            }
        }

    class Meta:
        model = DeviceInfo
        fields = ['id', 'code', 'latitude', 'longitude', 'sim', 'district']
