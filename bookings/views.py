from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

from bookings.serializers import BookingSerializer
from bookings.models import Booking

from seats.models import Seat
from slots.models import Slot
from django.db import transaction

# user_id 를 body로 하여 booking 추가 -> CreateModelMixin
class BookingViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    # user input : user_id(self.request.user.id), seat_id (body, 여러 개)
    # 1. create booking
    # 2. update seat state to 'payed' using booking ids
    # 3. increase reserved_seats in slot by one
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        booking = Booking.objects.create(user=request.user)
        seat_ids = request.data.get('seat_id')
        booking_info = []
        for seat_id in seat_ids:
            seat = Seat.objects.select_related('slot').select_related('slot__event').get(pk=seat_id)
            seat.state = 'payed'
            seat.booking = booking
            seat.save()

            # 서로 다른 이벤트를 저장할 수 있기 때문에 한 번에 증가시키지 않는다.
            slot = Slot.objects.select_for_update().get(pk=seat.slot.id)
            slot.reserved_seats += 1
            slot.save()

        return Response(data=BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


# user_id 기준 booking_id 가져오기 -> ListAPIView (여러 개)
# should populate seat information
class BookingByUserAPIVIew(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'user_id'

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        return Booking.objects.filter(user=user_id).prefetch_related('seats')