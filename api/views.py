from datetime import datetime

from django.db.models import OuterRef, Subquery
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

from api.serializers import UserSerializer, ConsumptionSerializer, DeviceInfoSerializer, \
    CitySerializer
from app import models
from app.models import Consumption, DeviceInfo, City, District, User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated]


class ConsumptionViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    API endpoint that allows consumption to be viewed.

    GET /consumption - get list of consumptions get last item of each device

    GET /consumption/<str:start_date_time>/<str:end_date_time>/<int:device_id>/
    get list of consumptions filtered by start_date_time, end_date_time and device_id

    """
    queryset = Consumption.objects.all().order_by('-updated_at')
    serializer_class = ConsumptionSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        try:
            # Get the URL parameters
            start_date_time = self.kwargs.get('start_date_time', None)
            end_date_time = self.kwargs.get('end_date_time', None)
            device_id = self.kwargs.get('device_id', None)

            # Convert URL parameters to aware datetime objects and set time to min or max
            start_date_time = datetime.combine(datetime.strptime(start_date_time, '%Y-%m-%d'), datetime.min.time()) \
                if start_date_time else None
            end_date_time = datetime.combine(datetime.strptime(end_date_time, '%Y-%m-%d'), datetime.max.time()) \
                if end_date_time else None

            # Check if all parameters are present
            if start_date_time and end_date_time and device_id:
                start_date_time = timezone.make_aware(start_date_time)
                end_date_time = timezone.make_aware(end_date_time)

                queryset = Consumption.objects.filter(
                    device_info_id=device_id,
                    updated_at__range=(start_date_time, end_date_time)
                ).order_by('-updated_at').all()

            else:
                # Get last item of each device by updated_at field (latest) and return queryset with this items only without distinct
                subquery = Consumption.objects.filter(device_info_id=OuterRef('device_info_id')).order_by('-updated_at')
                queryset = Consumption.objects.filter(id=Subquery(subquery.values('id')[:1])).order_by('-updated_at')
            return queryset
        except Exception as e:
            print(e)


class DeviceInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows device info to be viewed or edited.
    """
    queryset = DeviceInfo.objects.all().order_by('-updated_at')
    serializer_class = DeviceInfoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny]


class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows city to be viewed or edited.
    """
    queryset = City.objects.all().order_by('-updated_at')
    serializer_class = CitySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.AllowAny]
