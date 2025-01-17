from django.urls import path
from slots.views import SlotAPIView

urlpatterns = [
    path('', SlotAPIView.as_view()),
    path('<int:pk>/', SlotAPIView.as_view()),
]
