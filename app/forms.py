from django import forms

from .models import DeviceInfo


class DeviceInfoForm(forms.ModelForm):
    class Meta:
        model = DeviceInfo
        fields = '__all__'
