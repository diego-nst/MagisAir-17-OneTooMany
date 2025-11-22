from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flights',views.FlightsListView.as_view(), name='flights' )
]