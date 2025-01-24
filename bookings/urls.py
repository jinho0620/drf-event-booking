from django.urls import path
from rest_framework.routers import DefaultRouter

from bookings.views import BookingByUserAPIVIew, BookingViewSet

urlpatterns = [
    path('user/<int:user_id>/', BookingByUserAPIVIew.as_view(), name = 'booking_list_by_user_id'),
]

router = DefaultRouter()
router.register('', BookingViewSet)
urlpatterns += router.urls