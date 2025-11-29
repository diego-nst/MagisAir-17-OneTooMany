from django.contrib import admin
from .models import *

class RouteAdmin(admin.ModelAdmin):
    model = Route


class CityInLine(admin.TabularInline):
    model = City


class CityAdmin(admin.ModelAdmin):
    model = City


class PassengerAdmin(admin.ModelAdmin):
    model = Passenger


class PassengerInLine(admin.TabularInline):
    model = Passenger


class ItemAdmin(admin.ModelAdmin):
    model = Item


class RequestAdmin(admin.ModelAdmin):
    model = Request


class RequestInLine(admin.TabularInline):
    model = Request


class ItineraryAdmin(admin.ModelAdmin):
    model = Itinerary


class ItineraryInLine(admin.TabularInline):
    model = Itinerary


class AssignmentAdmin(admin.ModelAdmin):
    model = Assignment


class AssignmentInLine(admin.TabularInline):
    model = Assignment


class FlightAdmin(admin.ModelAdmin):
    model = Flight

    inlines = [ItineraryInLine, AssignmentInLine]


class BookingAdmin(admin.ModelAdmin):
    model = Booking

    inlines = [ItineraryInLine, RequestInLine]


class CrewAdmin(admin.ModelAdmin):
    model = Crew
    
    inlines = [AssignmentInLine,]




admin.site.register(City, CityAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Crew, CrewAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Itinerary, ItineraryAdmin)