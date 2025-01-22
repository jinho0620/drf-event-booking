from django.urls import path
from slots.views import SlotDetailAPIView, SlotAPIView

urlpatterns = [
    path('', SlotAPIView.as_view(), name='create_slot'),
    path('<int:pk>/', SlotAPIView.as_view(), name='delete_update_slot'),
    path('event/<int:event_id>/', SlotDetailAPIView.as_view(), name='slot_by_event_id'),
]
