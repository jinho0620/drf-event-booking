from django.urls import path
from rest_framework.routers import DefaultRouter

from seats.views import SeatBySlotAPIView, SeatByBookingAPIView, SeatViewSet, SeatReservationAPIView

urlpatterns = [
    path('slot/<int:slot_id>/', SeatBySlotAPIView.as_view(), name = 'seat_list_by_slot_id'),
    path('booking/<int:booking_id>/', SeatByBookingAPIView.as_view(), name = 'seat_list_by_booking_id'),
    path('<int:seat_id>/reserve/', SeatReservationAPIView.as_view(), name = 'reserve_seat'),
]

router = DefaultRouter()
router.register('', SeatViewSet)
urlpatterns += router.urls