from django.db import models

class FuelStation(models.Model):
    truckstop_name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=7,default=0.00)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state}"