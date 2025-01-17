from django.db import models
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from slots.models import Slot
from slots.serializers import SlotSerializer
from rest_framework import status

# Create your views here.
class SlotAPIView(APIView):
    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def post(self, request):
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk is not None:
            slot = Slot.objects.get(pk=pk)
            if slot is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = SlotSerializer(slot)
            return Response(serializer.data)

        slots = Slot.objects.all()
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            slot = Slot.objects.get(pk=pk)
            slot.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        slot = Slot.objects.get(pk=pk)
        if slot is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
