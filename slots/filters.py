import django_filters
from slots.models import Slot

class SlotFilterSet(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='start_at__date', lookup_expr='exact')
    event = django_filters.NumberFilter(field_name='event', lookup_expr='exact')

    class Meta:
        model = Slot
        fields = ('event', 'date')
