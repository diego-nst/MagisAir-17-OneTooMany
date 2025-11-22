from django import forms
from .models import Booking


class BookingsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []
