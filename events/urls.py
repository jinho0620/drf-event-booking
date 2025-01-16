from django.urls import path

from events.views import create_event, events_list, event_detail

urlpatterns = [
    path('', events_list),
    path('create/', create_event),
    path('<int:pk>/', event_detail),
]
