from django.db import models
from slots.models import Slot
from bookings.models import Booking
from seat_grades.models import Seat_grade

# Create your models here.
class Seat(models.Model):
    number = models.CharField(max_length=30)
    reserved = models.BooleanField()
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    seat_grade = models.ForeignKey(Seat_grade, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.number}'
