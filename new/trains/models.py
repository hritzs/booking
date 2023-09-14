

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Add related_name to resolve the clash
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='custom_users')

class Train(models.Model):
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seat_capacity = models.PositiveIntegerField()
    arrival_time_at_source = models.TimeField()
    arrival_time_at_destination = models.TimeField()

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    no_of_seats = models.PositiveIntegerField()
    seat_numbers = models.JSONField()
