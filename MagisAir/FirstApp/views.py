from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import *


# Create your views here.
def home(request):
    return render(request, 'home.html')

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
            for flight in Flight.objects.filter(route__origin__city_name__contains=originSearch, departure__gt=datetime.now()):
                results.add(flight)
        if destinationSearch and destinationSearch != "":
            temp_results = results
            results = set()
            for flight in Flight.objects.filter(route__destination__city_name__contains=destinationSearch, departure__gt=datetime.now()):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        temp_results = results
        results = set()
        if date_min_search != "" and date_max_search != "" and date_min_search and date_max_search:
            for flight in Flight.objects.filter(departure__gte=date_min_search,departure__lte=date_max_search, departure__gt=datetime.now()):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        elif date_min_search and date_min_search != "":
            for flight in Flight.objects.filter(departure__gte=date_min_search, departure__gt=datetime.now()):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        elif date_max_search and date_max_search != "":
            for flight in Flight.objects.filter(departure__lte=date_max_search, departure__gt=datetime.now()):
                if(flight in temp_results or not temp_results):
                    results.add(flight)
        else:
            results = temp_results
        
        current_passenger = Passenger.objects.get(profile=self.request.user.profile)
        ctx['pending_bookings'] =  Booking.objects.filter(passenger=current_passenger, paid=False)
        ctx['results'] = results
        searched = (originSearch != "" and originSearch != None) or (destinationSearch != "" and destinationSearch != None) or (date_min_search != "" and date_min_search != None) or (date_max_search != "" and date_max_search != None)
        ctx['searched'] = searched
        if not searched:
            ctx['results'] = Flight.objects.filter(departure__gt=datetime.now())
        return ctx
    
    def post(self, request, *args, **kwargs):
        itinerary = Itinerary()
        itinerary.flight = Flight.objects.get(flight_num=request.POST.get('flight'))
        itinerary.booking = Booking.objects.get(booking_id=request.POST.get('booking'))
        itinerary.save()
        itinerary.booking.total_cost += itinerary.flight.flight_cost
        itinerary.booking.save()
        return redirect(reverse_lazy('bookings:flights'))


from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

# assume these imports already exist in your file:
# from .models import Booking, Passenger, Itinerary, Flight, ...
# from Profile.models import Profile
# from .forms import BookingsCreate

class BookingsListView(LoginRequiredMixin, ListView):
    """
    View that lists all of a user's flight bookings
    """
    model = Booking
    template_name = 'bookings_list.html'
    form_class = BookingsCreate
    success_url = reverse_lazy('bookings_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # default empty values so template won't error
        context['unpaid_bookings'] = Booking.objects.none()
        context['paid_bookings'] = Booking.objects.none()
        context['bookings_create'] = BookingsCreate

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)

            # get the passenger (use .first() to be safe)
            passenger = Passenger.objects.filter(profile=profile).first()
            if not passenger:
                return context

            # fetch ALL bookings for this passenger once, ordered by booking_id
            all_user_bookings = list(
                Booking.objects.filter(passenger=passenger).order_by('booking_id')
            )

            # build a lookup: booking_id -> per-user number (1-based)
            booking_number_map = {
                b.booking_id: idx + 1 for idx, b in enumerate(all_user_bookings)
            }

            # fetch paid/unpaid sets (you already did this; keep same ordering as desired)
            unpaid_qs = Booking.objects.filter(passenger=passenger).exclude(paid=True)
            paid_qs = Booking.objects.filter(passenger=passenger).exclude(paid=False)

            # convert to lists so we can attach attributes
            unpaid_list = list(unpaid_qs)
            paid_list = list(paid_qs)

            # attach user_number attribute for template use: booking.user_number
            for b in unpaid_list:
                b.user_number = booking_number_map.get(b.booking_id, None)
            for b in paid_list:
                b.user_number = booking_number_map.get(b.booking_id, None)

            context['unpaid_bookings'] = unpaid_list
            context['paid_bookings'] = paid_list

        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            bookings_create = BookingsCreate(request.POST)

            if bookings_create.is_valid():
                booking = bookings_create.save(commit=False)
                passenger = Passenger.objects.filter(profile=profile).first()
                if passenger:
                    booking.passenger = passenger
                    booking.save()
                    return redirect('bookings:bookings_list')

        return self.get(request, *args, **kwargs)


class BookingsDetailView(DetailView):
    '''
    View that shows the details of one particular booking
    '''

    model = Booking
    template_name = 'bookings_detail.html'
    context_object_name = 'booking'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        booking = self.get_object()
        context['itineraries'] = Itinerary.objects.filter(booking=booking)

        return context


class BookingsUpdateView(UpdateView):
    '''
    View that allows the user to pay for a boooking
    '''

    model = Booking
    template_name = 'bookings_update.html'
    form_class = BookingsUpdate
    success_url = reverse_lazy('bookings:bookings_list')


class UserFlightsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'user_flights.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        passenger = get_object_or_404(Passenger, profile=profile)

        # Get bookings oldest first to assign fixed numbers
        bookings_oldest_first = Booking.objects.filter(passenger=passenger).order_by('booking_id')

        # Assign user-local numbers
        for idx, booking in enumerate(bookings_oldest_first, start=1):
            booking.user_number = idx

        # Now reverse the list so newest booking appears first
        bookings_descending = list(reversed(bookings_oldest_first))
        return bookings_descending