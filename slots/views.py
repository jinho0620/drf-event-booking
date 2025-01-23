from rest_framework import viewsets, generics
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser

from slots.filters import SlotFilterSet
from slots.models import Slot
from slots.serializers import SlotSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class SlotViewSet(
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SlotFilterSet # 구현 필요



    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


