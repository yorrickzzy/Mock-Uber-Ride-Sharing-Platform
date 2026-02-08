from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DriverProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Driver: {self.full_name} ({self.user.username})"


class Vehicle(models.Model):
    driver = models.OneToOneField(
        DriverProfile,
        on_delete=models.CASCADE
    )

    vehicle_type = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()
    special_info = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vehicle_type} - {self.license_plate}"
