from django.db import models

# Create your models here.
class Event(models.Model):
    class Category(models.TextChoices):
        'sports'
        'play'
        'musical'
        'concert'
        'orchestra'

    class State(models.TextChoices):
        'open'
        'closed'

    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    state = models.CharField(max_length=20, choices=State.choices) # should change to boolean

    def __str__(self):
        return f'{self.name}'
