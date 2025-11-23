from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import *


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
        date_min_search = self.request.GET.get('date_min')
        date_max_search = self.request.GET.get('date_max')        
        results = set()
        if originSearch and originSearch != "":
            for flight in Flight.objects.filter(route__origin__city_name__contains=originSearch):
                results.add(flight)
        if destinationSearch and destinationSearch != "":
            temp_results = results
            results = set()
            for flight in Flight.objects.filter(route__destination__city_name__contains=destinationSearch):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        temp_results = results
        results = set()
        if date_min_search != "" and date_max_search != "":
            for flight in Flight.objects.filter(departure__gte=date_min_search,departure__lte=date_max_search):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        elif date_min_search != "":
            for flight in Flight.objects.filter(departure__gte=date_min_search):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        elif date_max_search != "":
            for flight in Flight.objects.filter(departure__lte=date_max_search):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        ctx['results'] = results
        ctx['searched'] = originSearch != "" or destinationSearch != "" or date_min_search != "" or date_max_search != ""
        ctx['flights'] = Flight.objects.all()
        return ctx
    

class BookingsListView(LoginRequiredMixin, ListView):
    '''
    View that lists all of a user's flight bookings
    '''

    model = Booking
    template_name = 'bookings_list.html'
    form_class = BookingsCreate
    success_url = reverse_lazy('booking_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            passenger = Passenger.objects.filter(profile=profile)
            context['bookings'] = Booking.objects.filter(passenger=passenger).exclude(done_status=True)
        context['bookings_create'] = BookingsCreate

        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            bookings_create = BookingsCreate(request.POST)

            if bookings_create.is_valid():
                booking = bookings_create.save(commit=False)
                booking.passenger = Passenger.objects.filter(profile=profile)
                booking.save()

                return redirect('bookings_list')
            
        return self.get(request, *args, **kwargs)


class BookingsDetailView(DetailView):
    '''
    View that shows the details of one particular booking
    '''
    model = Booking
    template_name = 'bookings_detail.html'
    context_object_name = 'booking'
