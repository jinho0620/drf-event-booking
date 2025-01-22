from django.urls import path
from rest_framework.routers import DefaultRouter

from events import views

urlpatterns = [
    # path('', events_list.as_view(), name='events_list'),
    # path('search/', search_event),
    # path('create/', create_event),
    # path('<int:pk>/', event_detail),
    # path('popular/', events_booked_most.as_view(), name='get_most_booked_event_first'),
]

router = DefaultRouter()
router.register('', views.EventViewSet)
urlpatterns += router.urls