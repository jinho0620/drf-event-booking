from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from slots.models import Slot

class SlotSerializer(serializers.ModelSerializer):
    reserved_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = Slot
        fields = ('start_at', 'end_at', 'location', 'address', 'event', 'total_seats', 'reserved_seats', 'booking_rate')

    def validate(self, data):
        if data.get('start_at') < data.get('end_at'):
            return data
        else:
            raise ValidationError("start_at should be before end_at")

