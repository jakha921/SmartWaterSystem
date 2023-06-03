from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import DeviceInfo


class DeviceInfoForm(forms.ModelForm):
    class Meta:
        model = DeviceInfo
        fields = '__all__'


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        # type="text"
        # class="form-control"
        # id="email"
        # name="email-username"
        # placeholder="Enter your email or username"
        # autofocus

        'type': 'text',
        'class': 'form-control',
        'id': 'email',
        'name': 'email-username',
        'placeholder': 'Enter your email or username',
        'autofocus': 'autofocus',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'password',
        'id': 'password',
        'class': 'form-control',
        'name': 'password',
        'placeholder': 'Enter your password',
        'aria-describedby': 'password',
    }))
