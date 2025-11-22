from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flights',views.FlightsListView.as_view(), name='flights' ),
    path('bookings', views.BookingsListView.as_view, name='bookings_list'),
    path('booking/<int:pk>', views.BookingsDetailView.as_view(), name='bookings_detail')
]
