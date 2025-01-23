from django.db import models

# Create your models here.
class Slot(models.Model):
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    total_seats = models.PositiveIntegerField(default=0)
    reserved_seats = models.PositiveIntegerField(default=0)
    event = models.ForeignKey(to='events.Event', on_delete=models.SET_NULL, null=True, related_name='slots')

    def __str__(self):
        return f'{self.event} ({self.start_at} ~ {self.end_at})'

    @property
    def booking_rate(self):
        return self.reserved_seats / self.total_seats

    class Meta:
        ordering = ('start_at',) # 가장 빠른 것 부터 가져오기
        db_table = "slots"