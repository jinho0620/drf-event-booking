from datetime import timedelta, datetime

from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import status, mixins, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Case, When, FloatField, F, Value

from events.filters import OpenFilterBackend, EventFilterSet
from events.models import Event
from events.pagination import EventPagination
from events.serializers import EventSerializer, MostBookedEventSerializer
from django.db.models import Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection
# Create your views here.
# Use ModelViewSet
# Set permission_class [IsAuthenticated] for create method, other than that, [AllowAny]
# Get a keyword from query parameter to search

# 기간별 필터
# 최신순 정렬
# 오래된 순 정렬
# 카테고리별
# 예약률 높은 순
# state : closed 인 것 제외

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = EventPagination
    filter_backends = [OpenFilterBackend, SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = EventFilterSet
    search_fields = ['name', 'description', 'category', 'slots__location', 'slots__address']
    ordering_fields = ['created_at'] # ?ordering=(-)created_at (- is an option)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()




# 검색어 필터
# @api_view(['GET'])
# def search_event(request):
#     query = request.GET.get('query')
#     print(query)
#     if query is not None:
#         events = (Event.objects
#                   .filter(Q(name__icontains=query)
#                           | Q(description__icontains=query)
#                           | Q(category__icontains=query))
#                       .filter(open=True))
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)
#     else:
#         events = Event.objects.filter(open=True)
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)
#
# # 특정 기간을 기준으로 event 가져오기 -> 보통 정렬, 필터는 같이 적용하기 때문에 같은 api 로 해결 -> Class based view 사용
# # query param에 특정기간이 들어가면 queryset을 다르게 설정해줌 -> get_queryset() override필요
# class events_list(ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     filter_backends = [DjangoFilterBackend, OrderingFilter, OpenFilter]
#     filterset_fields = ['category']
#     ordering_fields = ['created_at']
#
#     def get_queryset(self):
#         start_date = self.request.query_params.get('start_date')
#         end_date = self.request.query_params.get('end_date')
#         print(type(end_date))
#         if start_date is not None and end_date is not None:
#             end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(1)
#             print(type(end_date))
#             # self.queryset = Event.objects.filter(Q(slots__start_at__gte=start_date) & Q(slots__start_at__lte=end_date)).distinct()
#             # print(end_date)
#             # slots_between_dates = Slot.objects.filter(start_at__gte=start_date).filter(end_at__lte=end_date)
#             # self.queryset = Event.objects.prefetch_related(Prefetch('slots', queryset=slots_between_dates, to_attr='slots_between_dates'))
#             # print(dir(self.queryset))
#         return super().get_queryset()
#
# class events_booked_most(ListAPIView):
#     queryset = Event.objects.annotate(
#         reserved_sum=Sum('slots__reserved_seats'),
#         total_sum=Sum('slots__total_seats'),
#         reservation_rate=Case(
#             When(reserved_sum=0, then=0),
#             default= F('reserved_sum') * 1.0 / F('total_sum'),
#             output_field=FloatField()
#             )
#         ).order_by('-reservation_rate')
#     serializer_class = MostBookedEventSerializer
