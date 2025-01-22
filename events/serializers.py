from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'category', 'start_at', 'end_at', 'open')

    def validate_category(self, value):
        categories = {'sports', 'play', 'musical', 'concert', 'orchestra'}
        if value in categories:
            return value
        raise ValidationError('The category should be one of the following. "sports", "play", "musical", "concert", "orchestra"')


    def validate(self, data):
        start_at = data.get('start_at')
        end_at = data.get('end_at')
        if start_at <= end_at:
            return data
        raise ValidationError('start_at should be before end_at')

class EventIncludingBookingRateSerializer(serializers.ModelSerializer):
    booking_rate = serializers.DecimalField(5, 2, read_only=True)

    class Meta:
        model = Event
        exclude = ('open',)