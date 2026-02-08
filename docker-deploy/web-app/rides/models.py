from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Rides(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_rides'
    )

    sharers = models.ManyToManyField(
        User,
        related_name='shared_rides',
        blank=True
    )

    vehicle = models.ForeignKey(
        'profiles.Vehicle',
        on_delete=models.SET_NULL,
        related_name='rides',
        null=True,
        blank=True
    )

    requested_time = models.DateTimeField()
    destination = models.CharField(max_length=255)
    num_passengers = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    is_shared = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    vehicle_type = models.CharField(max_length=50, blank=True)
    special_request = models.TextField(blank=True)

    def __str__(self):
        return f"Ride for {self.owner.username} to {self.destination} at {self.requested_time}"
