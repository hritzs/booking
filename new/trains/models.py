from django.db import models

# Create your models here.
class Train(models.Model):
    train_id = models.AutoField(primary_key=True)
    train_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    arrival_time_at_source = models.TimeField()
    arrival_time_at_destination = models.TimeField()