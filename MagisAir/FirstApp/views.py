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
    template_name = 'flights_list.html'

    def get_context_data(self, **kwargs):
        '''
        adds information to context if user is logged in
        displays commissions created and applied to
        '''
        ctx = super().get_context_data(**kwargs)

        ctx['flights'] = Flight.objects.all()
        return ctx

    