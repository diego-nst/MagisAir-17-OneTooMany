from django.urls import path
from . import views
from .views import UserFlightsView

urlpatterns = [
    path('', views.home, name='home'),
    path('flights',views.FlightsListView.as_view(), name='flights' ),
    path('bookings', views.BookingsListView.as_view(), name='bookings_list'),
    path('booking/<int:pk>', views.BookingsDetailView.as_view(), name='bookings_detail'),
    path('booking/<int:pk>/pay', views.BookingsUpdateView.as_view(), name='bookings_update'),
    path('userflights', UserFlightsView.as_view(), name='user_flights'),
]

app_name = 'bookings'