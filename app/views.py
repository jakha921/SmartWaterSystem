import re
import json
from datetime import datetime

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import OuterRef, Subquery
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, FormView

from app.forms import DeviceInfoForm, LoginForm
from app.models import Consumption, DeviceInfo


# Create your views here.
@csrf_exempt
def write_db(request):
    """
    Write data to database

    create regex pattern to validate data for
    {
        "code": "CzO3dzSkJ4",
        "data":
        {"total_pos": 2236168, "total_neg": -1412, "vaqt": "31052023 06:00:03"}
    }

    than check device info code exist in database or not if not create new device info and get id
    than create new consumption with device info id

    """
    pattern = r'"code":\s*"(?P<code>[^"]+)"[^}]+?"total_pos":\s*(?P<total_pos>[^,]+),\s*"total_neg":\s*(?P<total_neg>[^,]+),\s*"vaqt":\s*"(?P<vaqt>[^"]+)"'

    get_data = request.body.decode("utf-8")
    match = (re.search(pattern, get_data)).groupdict()
    if request.method == 'POST' and match:
        device_info = DeviceInfo.objects.filter(code=match['code']).first()
        print(device_info)
        if device_info is None:
            device_info = DeviceInfo.objects.create(code=match['code'])
        date_obj = datetime.strptime(match['vaqt'].replace(' ', ''), '%d%m%Y%H:%M:%S')
        match['vaqt'] = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        Consumption.objects.create(device_info=device_info, average_volume=match['total_pos'],
                                   volume=match['total_neg'], device_update_at=match['vaqt'])
        return JsonResponse({'status': 'ok'})
    else:
        return HttpResponseBadRequest()


def main(request):
    context = {
        'title': 'Main page',
        'active_page': 'main',
    }
    return render(request, 'app/main.html', context)


def index(request):
    return render(request, 'app/index.html')


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'app/auth-login-basic.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # Perform authentication or other necessary actions
            email_username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Perform authentication logic here

            user = authenticate(username=email_username, password=password)
            if user is not None:
                # A backend authenticated the credentials
                return redirect('tables')
            else:
                form.add_error(None, 'Invalid username or password')
                return render(request, 'app/auth-login-basic.html', {'form': form})
        else:
            return render(request, 'app/auth-login-basic.html', {'form': form})


def register(request):
    return render(request, 'app/auth-register.html')


def forgot_password(request):
    return render(request, 'app/auth-forgot-password-basic.html')


class TablesView( ListView):  # LoginRequiredMixin
    template_name = 'app/tables-basic.html'
    # login_url = '/login/'
    # redirect_field_name = '/tables/'
    context_object_name = 'consumptions'
    # paginate_by = 3

    def get_queryset(self):
        subquery = Consumption.objects.filter(device_info_id=OuterRef('device_info_id')).order_by('-updated_at')
        queryset = Consumption.objects.filter(id=Subquery(subquery.values('id')[:1])).order_by('-updated_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tables'
        context['active_page'] = 'tables'
        return context


class DevicesView(FormView):  # LoginRequiredMixin
    template_name = 'app/devices.html'
    form_class = DeviceInfoForm
    success_url = '/devices/'

    # login_url = '/login/'
    # redirect_field_name = 'devices'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = DeviceInfo.objects.all()
        context['title'] = 'Devices'
        context['active_page'] = 'devices'
        return context


def error(request):
    return render(request, 'app/pages-misc-error.html')


class UserListView(ListView):
    model = User
    template_name = 'app/users.html'
    context_object_name = 'users'
    paginate_by = 10
    ordering = ['-id']
    extra_context = {'title': 'Users'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'users'
        return context
