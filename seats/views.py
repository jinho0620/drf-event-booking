from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from seats.models import Seat
from seats.serializers import SeatSerializer
from rest_framework import status
from django.db import transaction

from slots.serializers import SlotSerializer
from slots.models import Slot

# 좌석 생성, 가져오기, 삭제, 정보 수정 (ex. 좌석 등급, 가격 수정)
# 좌석을 추가할 때 slots의 total_seats + 1
# 좌석을 삭제할 때 slots의 total_seats - 1
class SeatViewSet(ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    # def create(self, request, *args, **kwargs):
    #     seat_serializer = super().get_serializer(data=request.data)
    #     seat_serializer.is_valid(raise_exception=True)
    #     seat_serializer.save()
    #
    #     print(request.data)
    #     slot_id = request.data.get('slot')
    #     slot = Slot.objects.get(pk=slot_id)
    #     slot.total_seats += 1
    #     slot.save()
    #     return Response(seat_serializer.data, status=status.HTTP_201_CREATED)
    #
    # def destroy(self, request, *args, **kwargs):
    #     seat_id = kwargs.get('pk')
    #     seat = Seat.objects.get(pk=seat_id)
    #     slot_id = seat.slot.id
    #     seat.delete()
    #
    #     slot = Slot.objects.get(pk=slot_id)
    #     slot.total_seats -= 1
    #     slot.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# 좌석 예약 버튼을 눌렀을 때 호출, select_for_update()으로 동시성 처리
# concurrency test 완료
class SeatReservationAPIView(UpdateAPIView):
    serializer_class = SeatSerializer
    lookup_url_kwarg = 'seat_id'

    def get_queryset(self):
        return Seat.objects.select_for_update().get(pk=self.kwargs.get(self.lookup_url_kwarg))

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        seat = self.get_queryset()
        if seat.state == 'reserved' or seat.state == 'payed':
            return Response({'message': 'Seat already reserved'}, status=status.HTTP_404_NOT_FOUND)
        seat.state = 'reserved'
        seat.save()
        return Response({'error': 'Seat reserved successfully'}, status=status.HTTP_200_OK)


# (특정 행사의 특정 slot을) 예약할 때 좌석 정보 가져오기 -> 잔여 좌석 현황 (front에서 booking_id 가 OPEN이 아닌 것은 비활성화)
class SeatBySlotAPIView(ListAPIView):
    serializer_class = SeatSerializer
    lookup_url_kwarg = 'slot_id'

    def get_queryset(self):
        return Seat.objects.filter(slot=self.kwargs.get(self.lookup_url_kwarg))


# 행사 예약 내역을 확인할 때 좌석 정보 가져오기
class SeatByBookingAPIView(ListAPIView):
    serializer_class = SeatSerializer
    lookup_url_kwarg = 'booking_id'

    def get_queryset(self):
        return Seat.objects.filter(slot=self.kwargs.get(self.lookup_url_kwarg))