from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.views.generic.list import ListView


# Create your views here.
def home(request):
    return HttpResponse("Hello Django")

class FlightsListView(ListView):
    '''
    View that lists every available flight
    '''

    model = Flight

    