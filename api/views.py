from datetime import datetime

import jwt
from django.db.models import OuterRef, Subquery
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

from api.serializers import ConsumptionSerializer, DeviceInfoSerializer
from app import models
from app.models import Consumption, DeviceInfo, City, District, User
from config.settings import SECRET_KEY


class ConsumptionViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    API endpoint that allows consumption to be viewed.

    GET /consumption - get list of consumptions get last item of each device

    GET /consumption/<str:start_date_time>/<str:end_date_time>/<int:device_id>/
    get list of consumptions filtered by start_date_time, end_date_time and device_id

    """
    queryset = Consumption.objects.all().order_by('-updated_at')
    # authentication_classes = (TokenAuthentication,)
    serializer_class = ConsumptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_from_token_user_id(self):
        """
        Get user ID from the given token.
        :return: user_id or None if token is invalid or not provided
        """
        token = self.request.headers.get('Authorization', None)
        if token:
            try:
                # Remove the "Bearer " prefix from the token string
                token = token.split(' ')[1]
                decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token.get('user_id')
                return user_id
            except (jwt.DecodeError, jwt.InvalidTokenError):
                pass
        return None

    def get_queryset(self):
        try:
            user_id = self.get_from_token_user_id()
            city_id = None
            if user_id:
                user = User.objects.only('city_id').get(pk=user_id)
                city_id = user.city_id

            # Get the URL parameters
            start_date_time = self.kwargs.get('start_date', None)
            end_date_time = self.kwargs.get('end_date', None)
            device_id = self.kwargs.get('device_id', None)

            print('start_date_time', start_date_time)
            print('end_date_time', end_date_time)
            print('device_id', device_id)

            # Convert URL parameters to aware datetime objects and set time to min or max
            start_date_time = datetime.combine(datetime.strptime(start_date_time, '%Y-%m-%d'), datetime.min.time()) \
                if start_date_time else None
            end_date_time = datetime.combine(datetime.strptime(end_date_time, '%Y-%m-%d'), datetime.max.time()) \
                if end_date_time else None

            # Get the base queryset
            queryset = Consumption.objects.all().order_by('-updated_at')

            if start_date_time and end_date_time and device_id:
                start_date_time = timezone.make_aware(start_date_time)
                end_date_time = timezone.make_aware(end_date_time)

                # Filter the queryset based on the parameters
                queryset = queryset.filter(
                    device_info_id=device_id,
                    updated_at__range=(start_date_time, end_date_time)
                )

            elif not (start_date_time and end_date_time and device_id):
                # Create a subquery to get the last item IDs of each device
                subquery = Consumption.objects.filter(device_info_id=OuterRef('device_info_id')).order_by('-updated_at')
                subquery = subquery.values('id')[:1]

                if city_id:
                    # Filter the base queryset based on the subquery results and city ID
                    queryset = queryset.filter(
                        id__in=Subquery(subquery),
                        device_info__district_id__city_id=city_id
                    ).order_by('-device_info__district__name_ru')
                else:
                    # Filter the base queryset based on the subquery results
                    queryset = queryset.filter(id__in=Subquery(subquery))

            return queryset

        except Exception as e:
            print(e)
            return []


class DeviceInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows device info to be viewed or edited.
    """
    queryset = DeviceInfo.objects.all().order_by('-updated_at')
    serializer_class = DeviceInfoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
