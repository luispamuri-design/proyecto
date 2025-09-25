from django import forms
from .models import Appointment, Service

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['owner_name','pet_name','pet_type','service','date_time','phone','email']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type':'datetime-local'}),
        }
