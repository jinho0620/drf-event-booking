from rest_framework import filters
import django_filters
from events.models import Event

class OpenFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(open=True)

# category
#
class EventFilterSet(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    start_at = django_filters.DateFromToRangeFilter(field_name='slots__start_at__date')

    class Meta:
        model = Event
        # fields = {'category': ['iexact']}
        fields = ('category',)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset) # filtering the queryset from the view and BaseFilterBackend
        print(queryset)
        return queryset.distinct()


