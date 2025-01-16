from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'category', 'state')

    def validate_category(self, value):
        categories = {'sports', 'play', 'musical', 'concert', 'orchestra'}
        if value in categories:
            return value
        raise ValidationError('The category should be one of the following. "sports", "play", "musical", "concert", "orchestra"')

    def validate_state(self, value):
        states = {'open', 'closed'}
        if value in states:
            return value
        raise ValidationError('The states should be either "open" or "closed"')



