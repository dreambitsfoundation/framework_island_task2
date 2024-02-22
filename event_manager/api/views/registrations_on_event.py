from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.models import EventRegistration
from api.serializers import EventRegistrationSerializer

class RegistrationOnEventsView(ModelViewSet):
    """
    This view returns all the registration record with
    respect to an event.

    Rule: The requesting user has to be a staff user to see it.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ['get']
    serializer_class = EventRegistrationSerializer

    def list(self, request, pk, *args, **kwargs):
        """ Takes an event ID as input and returns all the active and inactive event registrations. """
        queryset = EventRegistration.objects.filter(event__pk=pk).order_by('-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)