from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from events.models import Event
from events.serializers import EventSerializer


# Create your views here.
@api_view(['POST'])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def events_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(['GET', 'DELETE', 'PATCH'])
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk) # should customize exception

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)