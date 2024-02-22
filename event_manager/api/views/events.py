from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from event_manager.exceptions import APIError
from api.models import Event, EventRegistration
from api.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    
    def update(self, request, pk, *args, **kwargs):
        if "capacity" in request.data:
            registrations = EventRegistration.objects.filter(event__pk=pk, is_active=True)
            if registrations.count() > request.data.get("capacity"):
                raise APIError("Provided capacity value is smaller then existing registration count on this event")
        return super().update(request, pk, *args, **kwargs)

    