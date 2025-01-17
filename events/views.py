from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from events.models import Event
from events.serializers import EventSerializer
from django.db.models import Q

# Create your views here.
@api_view(['POST'])
def create_event(request):
    # print(request.user.is_staff)
    # print(request.user.is_anonymous)
    # print(dir(request.successful_authenticator))
    # print(dir(request.auth))
    # print(dir(request.authenticators))
    if request.user.is_authenticated:
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

# 최신순 정렬
# 오래된 순 정렬
# 카테고리별
# state : closed 인 것 제외
# 기간별 필터 -> slot에서 가능
@api_view(['GET'])
def events_list(request):
    ordering = request.GET.get('ordering')
    category = request.GET.get('category')
    if ordering == 'oldest':
        if category is not None:
            events = Event.objects.filter(open=True).filter(category=category).order_by('created_at')
        else:
            events = Event.objects.filter(open=True).order_by('created_at')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    elif ordering == 'newest' or ordering is None:
        if category is not None:
            events = Event.objects.filter(open=True).filter(category=category)
        else:
            events = Event.objects.filter(open=True)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'DELETE', 'PATCH'])
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, open=True) # should customize exception

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        event.open = False
        event.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 검색어 필터
@api_view(['GET'])
def search_event(request):
    query = request.GET.get('query')
    print(query)
    if query is not None:
        events = (Event.objects
                  .filter(Q(name__icontains=query)
                          | Q(description__icontains=query)
                          | Q(category__icontains=query))
                  .filter(open=True))
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    else:
        events = Event.objects.filter(open=True)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)