from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import DriverProfile, Vehicle

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['full_name','is_active']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'license_plate', 'capacity', 'special_info']
        widgets = {
            'special_info': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
