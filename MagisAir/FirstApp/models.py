from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.city_name
    
    class Meta:
        verbose_name_plural = 'Cities'


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    duration = models.DurationField()
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

    def __str__(self):
        return self.origin.__str__() +"-"+ self.destination.__str__()


class Flight(models.Model):
    flight_num = models.AutoField(primary_key=True)
    departure = models.DateTimeField(default=datetime.now)
    arrival = models.DateTimeField(default=datetime.now)
    flight_date = models.DateField(default=datetime.now)
    flight_cost = models.FloatField(validators=[MinValueValidator(0)])
    route = models.ForeignKey(
        Route,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.route.__str__()+" - "+ str(self.pk)


class Crew(models.Model):
    crew_id = models.AutoField(primary_key=True)
    crew_name = models.CharField(max_length=255)

    def __str__(self):
        return self.crew_name


class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255)
    flight = models.ForeignKey(
        Flight,
        on_delete = models.CASCADE
    )
    crew = models.ForeignKey(
        Crew,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.crew.__str__() + " in " +self.flight.__str__()


class Passenger(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=2)
    birth_date = models.DateField(default=datetime.now)
    gender = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    total_cost = models.FloatField(validators=[MinValueValidator(0)])
    booking_date = models.DateField(auto_now=True)
    passenger = models.ForeignKey(
        Passenger,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.passenger.__str__() + " " + self.booking_id


class Item(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    item_cost = models.FloatField(validators=[MinValueValidator(0)])
    booking = models.ForeignKey(
        Booking,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.description + " - " + self.booking.__str__()
    
    class Meta:
        verbose_name_plural = 'Itineraries'


class Itinerary(models.Model):
    flight = models.ForeignKey(
        Flight,
        on_delete = models.CASCADE
    )
    booking = models.ForeignKey(
        Booking,
        on_delete = models.CASCADE
    )

    def __str__(self):
        return self.flight.__str__() + " " + self.booking.__str__()
    
    class Meta:
        verbose_name_plural = 'Itineraries'
