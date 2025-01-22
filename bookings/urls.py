from django.urls import path

from bookings.views import BookingByUserAPIVIew, BookingCreateAPIView, BookingDeleteAPIView

urlpatterns = [
    path('', BookingCreateAPIView.as_view(), name = 'create_booking'),
    path('<int:pk>/', BookingDeleteAPIView.as_view(), name = 'delete_booking'),
    path('user/<int:user_id>/', BookingByUserAPIVIew.as_view(), name = 'booking_list_by_user_id'),
]