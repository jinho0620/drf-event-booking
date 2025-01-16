from django.db import models
from events.models import Event

# Create your models here.
class Slot(models.Model):
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.event} ({self.start_at} ~ {self.end_at})'
