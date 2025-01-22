from rest_framework import filters
import django_filters
from events.models import Event
from django.db.models import Sum, F, When, Case, FloatField

# 기본 설정 (현재 열려 있는 행사만 가져오기)
class OpenFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(open=True)

# 캬테고리 및 기간 설정
class EventFilterSet(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    start_at = django_filters.DateFromToRangeFilter(field_name='slots__start_at__date')

    class Meta:
        model = Event
        # fields = {'category': ['iexact']}
        fields = ('category',)

    def filter_queryset(self, queryset):
        if self.request.query_params.get('start_at'):
            queryset = super().filter_queryset(queryset) # filtering the queryset from the view and BaseFilterBackend
            return queryset.distinct()
        return queryset

# 예약률 기준 정렬
class BookingRateOrderingFilter(filters.OrderingFilter):
    ordering_fields = ['booking_rate']

    def filter_queryset(self, request, queryset, view):
        queryset = queryset.annotate(
                reserved_seats_sum=Sum('slots__reserved_seats'),
                total_seats_sum=Sum('slots__total_seats'),
                booking_rate=Case (
                    When(reserved_seats_sum=0, then=0),
                    default=F('reserved_seats_sum') * 1.0 / F('total_seats_sum'),
                    output_field=FloatField()
                )
        )

        ordering = request.query_params.get('ordering')
        if ordering in ['booking_rate', '-booking_rate']:
            queryset = queryset.order_by(ordering)

        print(queryset.query)
        return queryset



