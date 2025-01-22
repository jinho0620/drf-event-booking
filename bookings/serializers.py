from rest_framework import serializers
from bookings.models import Booking
from seats.serializers import SeatSerializer
from seats.models import Seat


class BookingSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(read_only=True, many=True)
    total_seats = serializers.SerializerMethodField(method_name='get_total_seats')
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_seats(self, obj):
        return len(obj.seats.all())

    def get_total_price(self, obj):
        return sum(seat.price for seat in obj.seats.all())

    class Meta:
        model = Booking
        fields = ('id', 'seats', 'total_seats', 'total_price')


