from django.urls import path

from bookings.views import BookingByUserAPIVIew, BookingAPIView

urlpatterns = [
    path('', BookingAPIView.as_view(), name = 'create_delete_retrieve_booking'),
    path('user/<int:user_id>/', BookingByUserAPIVIew.as_view(), name = 'booking_list_by_user_id'),
]