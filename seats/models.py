from django.db import models

# Create your models here.
class Seat(models.Model):
    class State(models.TextChoices):
        OPEN = 'open'
        RESERVED = 'reserved'
        PAYED = 'payed'

    number = models.CharField(max_length=30)
    grade = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    state = models.CharField(max_length=20, choices=State.choices, default=State.OPEN)
    slot = models.ForeignKey(to='slots.Slot', on_delete=models.CASCADE)
    booking = models.ForeignKey(to='bookings.Booking', on_delete=models.SET_NULL, null=True, related_name='seats')


    def __str__(self):
        return f'{self.number}'

    class Meta:
        db_table = "seats"