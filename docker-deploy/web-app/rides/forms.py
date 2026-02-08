from django import forms
from django.forms import ModelForm
from .models import Rides

class RequestRideForm(forms.ModelForm):
    num_passengers = forms.IntegerField(
        widget = forms.NumberInput(attrs={'min': 1, 'class': 'form-control'})
    )
    class Meta:
        model = Rides
        fields = ['destination', 'requested_time', 'num_passengers', 'is_shared','vehicle_type','special_request',]
        widgets = {
            'requested_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'special_request': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }
