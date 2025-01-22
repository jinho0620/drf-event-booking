from django.db import models

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(to='users.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        db_table = "bookings"