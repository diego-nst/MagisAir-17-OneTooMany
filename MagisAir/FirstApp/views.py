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
        ctx = super().get_context_data(**kwargs)
        originSearch = self.request.GET.get('search')
        if originSearch:
            ctx['results'] = Flight.objects.filter(route__origin__city_name__contains=originSearch)
        ctx['flights'] = Flight.objects.all()
        return ctx

    