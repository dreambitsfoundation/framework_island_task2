from django.contrib.auth.models import User
from rest_framework import serializers

from .models import EventRegistration, Event
from authentication.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=False, required=False)
    capacity = serializers.IntegerField(read_only=False, required=False)
    
    class Meta:
        model = Event
        fields = "__all__"


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = "__all__"
        
    def to_representation(self, instance):
        data = super(EventRegistrationSerializer, self).to_representation(instance)
        modified_fields = {
            "booked_by": UserSerializer(instance=User.objects.get(pk=data.get("booked_by")), many=False).data,
            "event": EventSerializer(instance=Event.objects.get(pk=data.get("event")), many=False).data
        }
        data.update(modified_fields)
        return data

