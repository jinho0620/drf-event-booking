from django.urls import path
from slots.views import SlotDetailAPIView

urlpatterns = [
    # path('', SlotAPIView.as_view(), name='create_delete_slot'),
    path('event/<int:event_id>/', SlotDetailAPIView.as_view(), name='slot_by_event_id'),
    # path('<int:pk>/', SlotAPIView.as_view(), name='update_slot'),
]
