from django.urls import path
from rest_framework.routers import DefaultRouter

from slots.views import SlotViewSet

urlpatterns = [
]

router = DefaultRouter()
router.register('', SlotViewSet)
urlpatterns += router.urls
