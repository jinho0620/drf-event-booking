from django.urls import path

from events.views import create_event, events_list, event_detail, search_event

urlpatterns = [
    path('', events_list),
    path('search/', search_event),
    path('create/', create_event),
    path('<int:pk>/', event_detail),
]
