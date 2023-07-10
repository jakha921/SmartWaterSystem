import re
import json
from datetime import datetime

import pytz
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.defaultfilters import lower
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import OuterRef, Subquery
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, FormView, DetailView

from app.forms import DeviceInfoForm
from app.models import Consumption, DeviceInfo, District, City


# Create your views here.
@csrf_exempt
def write_db(request):
    """
    Write data to database

    create regex pattern to validate data for
    {
        "code": "CzO3dzSkJ4",
        "data":
        {"total_pos": 2236168, "total_neg": -1412, "vaqt": "31052023 06:00:03"} or
        {"total_pos": 2236168, "total_neg": -1412, "vaqt": "20230625155108"}
    }

    than check device info code exist in database or not if not create new device info and get id
    than create new consumption with device info id

    """
    if request.method == 'POST':
        pattern = r'"code":\s*"(?P<code>[^"]+)"[^}]+?"total_pos":\s*(?P<total_pos>[^,]+),\s*"total_neg":\s*(?P<total_neg>[^,]+),\s*"vaqt":\s*"(?P<vaqt>[^"]+)"'

        get_data = request.body.decode("utf-8")
        match = (re.search(pattern, get_data)).groupdict()
        if match:
            device_info = DeviceInfo.objects.filter(code=match['code']).first()
            if device_info is None:
                device_info = DeviceInfo.objects.create(code=match['code'])

            try:
                match['vaqt'] = datetime.strptime(match['vaqt'], '%d%m%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except:
                match['vaqt'] = datetime.strptime(match['vaqt'], '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')

            timezone = pytz.timezone('Asia/Tashkent')
            match['vaqt'] = timezone.localize(datetime.strptime(match['vaqt'], '%Y-%m-%d %H:%M:%S'))

            print(device_info, match['vaqt'])
            # set tatol_neg if tatol_neg < 0 set abs value
            print('before', match['total_neg'])
            if int(float(match['total_neg'])) < 0:
                match['total_neg'] = abs(int(match['total_neg']))
            print('after', match['total_neg'])
            Consumption.objects.create(device_info=device_info, average_volume=match['total_pos'],
                                       volume=match['total_neg'], device_update_at=match['vaqt'])

            return JsonResponse({'status': 'ok'})
        else:
            return HttpResponseBadRequest()

    if request.method == 'GET':
        return redirect('app:tables')


def main(request):
    # get all devices_info ids where device_info_id is in consumption table
    subquery = Consumption.objects.filter(device_info_id=OuterRef('device_info_id')).order_by('-updated_at')
    # get all consumption where id is in subquery
    queryset = Consumption.objects.filter(id=Subquery(subquery.values('id')[:1])).order_by('-updated_at')
    # get all device_info where id is in subquery
    devices = DeviceInfo.objects.filter(id__in=queryset.values_list('device_info_id', flat=True))

    context = {
        'title': 'Main page',
        'active_page': 'main',
        'devices': devices
    }
    return render(request, 'app/main.html', context)


def index(request):
    return render(request, 'app/index.html')


class TablesView(LoginRequiredMixin, ListView):
    template_name = 'app/tables-basic.html'
    login_url = '/auth/login/'
    context_object_name = 'consumptions'

    # paginate_by = 3

    def get_queryset(self):

        subquery = Consumption.objects.filter(device_info_id=OuterRef('device_info_id')).order_by('-updated_at')
        if self.request.user.city_id:
            # get ids of all discricts where city id is self.request.user.city_id
            district_id_list = District.objects.filter(city_id=self.request.user.city_id).values_list('id', flat=True)
            # order by city name_ru

            queryset = Consumption.objects.filter(
                id=Subquery(subquery.values('id')[:1]),
                device_info__district_id__in=district_id_list.values_list('id', flat=True)
            ).order_by('-device_info__district__name_ru', '-device_info__district__city__name_ru', 'device_info__object_name')
        else:
            queryset = Consumption.objects.filter(id=Subquery(subquery.values('id')[:1])).order_by(
                '-device_info__district__city__name_ru', '-device_info__district__name_ru', 'device_info__object_name')
        numbered_queryset = enumerate(queryset, 1)
        return numbered_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Table'
        context['active_page'] = 'tables'
        return context


class DevicesView(LoginRequiredMixin, FormView):
    template_name = 'app/devices.html'
    form_class = DeviceInfoForm
    success_url = '/devices/'
    login_url = '/auth/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = DeviceInfo.objects.all()
        context['title'] = 'Devices'
        context['active_page'] = 'devices'
        return context


class ConsumptionView(LoginRequiredMixin, View):
    template_name = 'app/consumptions-detail.html'
    login_url = '/auth/login/'

    def get(self, request, *args, **kwargs):
        subquery = Consumption.objects.filter(device_info_id=OuterRef('device_info_id')).order_by('-updated_at')
        queryset = Consumption.objects.filter(id=Subquery(subquery.values('id')[:1]),
                                              device_info__district__city_id=self.kwargs['pk']).order_by(
            '-device_info__district__name_ru', '-device_info__district__city__name_ru', 'device_info__object_name')
        if queryset.count() == 0:
            return redirect('app:tables')

        context = {
            'title': 'Consumption',
            'active_page': queryset.first().device_info.district.city.name_en,
            'consumptions': queryset
        }
        return render(request, self.template_name, context)

def error(request):
    return render(request, 'app/pages-misc-error.html')


class UserListView(ListView):
    model = User
    template_name = 'app/users.html'
    context_object_name = 'users'
    # paginate_by = 10
    ordering = ['-id']
    extra_context = {'title': 'Users'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'users'
        return context


def pagination(request):
    return render(request, 'app/ui-pagination-breadcrumbs.html')
