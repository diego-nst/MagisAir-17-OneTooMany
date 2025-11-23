from django import forms
from .models import Booking


class BookingsCreate(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []

class BookingsUpdate(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['done_status']
