from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=255)
    longitude = models.IntegerField
    latitude = models.IntegerField


class Route(models.Model):
    duration = models.DurationField
    origin = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='departures'
    )
    destination = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='arrivals'
    )


class Flight(models.Model):
    departure = models.DateTimeField
    arrival = models.DateTimeField
    flight_date = models.DateField
    flight_cost = models.IntegerField
    route = models.ForeignKey(
        Route,
        on_delete = models.CASCADE
    )


class Crew(models.Model):
    crew_name = models.CharField(max_length=255)


class Assignment(models.Model):
    role = models.CharField(max_length=255)
    flight = models.ForeignKey(
        Flight,
        on_delete = models.CASCADE
    )
    crew = models.ForeignKey(
        Crew,
        on_delete = models.CASCADE
    )


class Passenger(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=2)
    birth_date = models.DateField
    gender = models.CharField(max_length=255)


class Booking(models.Model):
    total_cost = models.IntegerField
    booking_date = models.DateField
    passenger = models.ForeignKey(
        Passenger,
        on_delete = models.CASCADE
    )


class Item(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.IntegerField
    item_cost = models.IntegerField
    booking = models.ForeignKey(
        Booking,
        on_delete = models.CASCADE
    )


class Itinerary(models.Model):
    flight = models.ForeignKey(
        Flight,
        on_delete = models.CASCADE
    )
    booking = models.ForeignKey(
        Booking,
        on_delete = models.CASCADE
    )
