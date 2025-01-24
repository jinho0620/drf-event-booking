from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from events.exceptions import EventNotFoundException
from events.filters import OpenFilterBackend, EventFilterSet, BookingRateOrderingFilter
from events.models import Event
from events.pagination import EventPagination
from events.serializers import EventSerializer, EventIncludingBookingRateSerializer
from django_filters.rest_framework import DjangoFilterBackend

# 필터
# 기간별 필터
# 카테고리별
# 검색어

# 정렬
# 최신순 정렬
# 오래된 순 정렬
# 예약률 높은 순

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination
    filter_backends = [OpenFilterBackend, SearchFilter, DjangoFilterBackend, OrderingFilter, BookingRateOrderingFilter] # order-sensitive, DjangoFilterBackend : for FilterSet
    filterset_class = EventFilterSet
    search_fields = ['name', 'description', 'category', 'slots__location', 'slots__address']
    ordering_fields = ['created_at'] # ?ordering=(-)created_at (- is an option)
    ordering = ['-created_at'] # for testing, already exists in model

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        ordering = self.request.query_params.get('ordering')
        if ordering in ['booking_rate', '-booking_rate']:
            self.serializer_class = EventIncludingBookingRateSerializer
        return super().get_serializer_class()

    # def retrieve(self, request, *args, **kwargs):
    #     event_id = kwargs.get('pk')
    #     try:
    #         event = Event.objects.get(pk=event_id)
    #     except Event.DoesNotExist:
    #         raise EventNotFoundException()
    #     serializer = super().get_serializer(event)
    #     return Response(serializer.data)