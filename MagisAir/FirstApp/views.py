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
        originSearch = self.request.GET.get('origin')
        destinationSearch = self.request.GET.get('destination')
        results = set()
        searched = False
        if originSearch and originSearch != "":
            for flight in Flight.objects.filter(route__origin__city_name__contains=originSearch):
                results.add(flight)
        if destinationSearch and destinationSearch != "":
            temp_results = results
            results = set()
            for flight in Flight.objects.filter(route__destination__city_name__contains=destinationSearch):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        ctx['results'] = results
        ctx['searched'] = originSearch != "" or destinationSearch != ""
        ctx['flights'] = Flight.objects.all()
        return ctx

    