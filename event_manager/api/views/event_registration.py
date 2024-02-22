from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from authentication.serializers import UserSerializer

from event_manager.exceptions import APIError
from api.models import EventRegistration, Event
from api.serializers import EventRegistrationSerializer, EventSerializer

class EventRegistrationView(viewsets.ModelViewSet):
    """
    This view is responsible for handling event registration
    """
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated]
    queryset = EventRegistration.objects.all().order_by('-created_at')
    serializer_class = EventRegistrationSerializer

    def create(self, request, *args, **kwargs):
        """
        This method is used to retrieve single event registration/booking.
        """
        # Check if this registration will go beyond the capacity
        if not self.can_take_one_more_registration(event_pk=request.data.get("event")):
            raise APIError("We're sold out for this event. Can't accomodate any more bookings.", status_code=status.HTTP_226_IM_USED)
        request.data['booked_by'] = request.user.pk
        event_registration_serialized = EventRegistrationSerializer(data=request.data)
        if event_registration_serialized.is_valid():
            event_registration_serialized.save()
            return Response(event_registration_serialized.data, status=status.HTTP_201_CREATED)
        else:
            raise APIError(event_registration_serialized.errors)

    def retrieve(self, request, pk, *args, **kwargs):
        """
        This method is used to retrieve single event registration/booking

        Rule: A staff user can see any record and standard 
        user can see only see their own bookings/registrations.
        """
        if not request.user.is_staff:
            event_registration = EventRegistration.objects.get(pk=pk)
            if event_registration.booked_by != request.user:
                raise APIError("You are not authorized to view this data.", status_code=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, pk, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        """
        This method is used to list all event registration/booking

        Rule: A staff user can see all records and standard 
        user can see only see their own bookings/registrations.
        """
        if not request.user.is_staff:
            self.queryset = EventRegistration.objects.filter(booked_by=request.user).order_by('-created_at')
        return super().list(request, *args, **kwargs)
    
    def destroy(self, request, pk, *args, **kwargs):
        """
        This method is used to cancel a event registration/booking
        by setting is_active = False. 

        Rule: This operation can only be performed by a staff user or
        the owner of the registration.
        """
        event_registration = EventRegistration.objects.get(pk=pk)
        if request.user.is_staff or event_registration.booked_by == request.user:
            event_registration.is_active = False
            event_registration.save()
            return Response({"message": "Event registration cencelled."}, status=status.HTTP_410_GONE)
        else:
            raise APIError("You are not authorized to perform this operation.", status_code=status.HTTP_403_FORBIDDEN)
        
    def can_take_one_more_registration(self, event_pk: str):
        current_registrations = EventRegistration.objects.filter(event__pk=event_pk, is_active=True)
        event = Event.objects.get(pk = event_pk)
        if current_registrations.count() < event.capacity:
            return True
        return False