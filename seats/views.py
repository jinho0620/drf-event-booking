from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from seats.models import Seat
from seats.serializers import SeatSerializer
from rest_framework import status
from django.db import transaction, DatabaseError

from slots.serializers import SlotSerializer
from slots.models import Slot

# 좌석 생성, 가져오기, 삭제
# 좌석 정보 수정 (ex. 좌석 등급, 가격 수정)
class SeatViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# 좌석 예약 버튼을 눌렀을 때 호출, select_for_update()으로 동시성 처리
class SeatReservationAPIView(UpdateAPIView):
    serializer_class = SeatSerializer
    lookup_url_kwarg = 'seat_id'

    # 예약 버튼 경쟁에서 lock 을 못 얻었을 때 바로 실패시키기 위해 nowait=True
    def get_queryset(self):
        return Seat.objects.select_for_update(nowait=True)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        seat_id = self.kwargs.get(self.lookup_url_kwarg)
        try:
            seat = self.get_queryset().get(pk=seat_id)
        except Seat.DoesNotExist:
            return Response({'message': 'The seat is not found'}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({'message': 'Someone is already booking'}, status=status.HTTP_409_CONFLICT)

        if seat.state in ['reserved', 'payed']:
            return Response({'message': 'The seat is already reserved'}, status=status.HTTP_400_BAD_REQUEST)

        seat.state = 'reserved'
        seat.save()
        return Response({'error': 'Seat reserved successfully'}, status=status.HTTP_200_OK)


# (특정 행사의 특정 slot을) 예약할 때 좌석 정보 가져오기 -> 잔여 좌석 현황 (front에서 booking_id 가 OPEN이 아닌 것은 비활성화)
class SeatBySlotAPIView(ListAPIView):
    serializer_class = SeatSerializer
    lookup_url_kwarg = 'slot_id'

    def get_queryset(self):
        slot_id = self.kwargs.get(self.lookup_url_kwarg)
        return Seat.objects.filter(slot=slot_id)


# 행사 예약 내역을 확인할 때 좌석 정보 가져오기
class SeatByBookingAPIView(ListAPIView):
    serializer_class = SeatSerializer
    lookup_url_kwarg = 'booking_id'

    def get_queryset(self):
        booking_id = self.kwargs.get(self.lookup_url_kwarg)
        return Seat.objects.filter(booking=booking_id)