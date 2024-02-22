import json
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate

from django.test import TestCase
from django.contrib.auth.models import User

from api.models import Event, EventRegistration
from api.serializers import EventSerializer, EventRegistrationSerializer
from api.views import EventViewSet, EventRegistrationView, RegistrationOnEventsView

TEST_CONTENT_DIRECTORY = "api/tests/test_elements"
TEST_USER_CONTENT_DIRECTORY = "authentication/tests/test_elements"


class TestEventView(TestCase):
    """This is the test suite for Event View"""

    def setUp(self) -> None:
        event_payload = open(f"{TEST_CONTENT_DIRECTORY}/event_payload.json")
        self.event_payload = json.load(event_payload)

        payload = open(f"{TEST_USER_CONTENT_DIRECTORY}/user.json")
        self.user_payload = json.load(payload)

         # Create an admin user
        admin_user = User(**self.user_payload[0])
        admin_user.set_password(self.user_payload[0].get("password"))
        admin_user.is_staff = True
        admin_user.save()
        self.admin_user = admin_user

        # Create a standard user
        standard_user = User(**self.user_payload[1])
        standard_user.set_password(self.user_payload[1].get("password"))
        standard_user.is_staff = False
        standard_user.save()
        self.standard_user = standard_user
    
    def test_create_event(self):
        view = EventViewSet.as_view({'post': 'create'})

        # Request with Admin User pass successfully.
        client = APIRequestFactory()
        request = client.post('/api/event/', json.dumps(self.event_payload[0]), content_type='application/json')
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

        # Request with Standard User fail.
        client = APIRequestFactory()
        request = client.post('/api/event/', json.dumps(self.event_payload[1]), content_type='application/json')
        force_authenticate(request, user=self.standard_user)
        response = view(request)
        self.assertEqual(response.status_code, 403)

    def test_event_individual(self):
        view = EventViewSet.as_view({'get': 'retrieve'})
        
        # Create dummy events
        # Event with higher capacity
        self.event_higher_capacity = Event(**self.event_payload[0])
        self.event_higher_capacity.save()

        # Event with lower capacity
        self.event_lower_capacity = Event(**self.event_payload[1])
        self.event_lower_capacity.save()

        # Make API call to get the event data
        client = APIRequestFactory()
        request = client.get(f'/api/event/')
        force_authenticate(request, user=self.admin_user)
        response = view(request, pk=str(self.event_higher_capacity.pk))
        self.assertEqual(response.status_code, 200)

        serialized_event = EventSerializer(instance=self.event_higher_capacity, many=False)
        self.assertDictEqual(response.data, serialized_event.data)

    def test_event_list(self):
        view = EventViewSet.as_view({'get': 'list'})
        
        # Create dummy events
        # Event with higher capacity
        self.event_higher_capacity = Event(**self.event_payload[0])
        self.event_higher_capacity.save()

        # Event with lower capacity
        self.event_lower_capacity = Event(**self.event_payload[1])
        self.event_lower_capacity.save()

        # Make API call to get the event data
        client = APIRequestFactory()
        request = client.get(f'/api/event/', content_type='application/json')
        force_authenticate(request, user=self.admin_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), 2)
    
    
class TestEventRegistrationView(TestCase):
    """This is the test suite for Event View"""

    def setUp(self) -> None:
        event_payload = open(f"{TEST_CONTENT_DIRECTORY}/event_payload.json")
        self.event_payload = json.load(event_payload)

        payload = open(f"{TEST_USER_CONTENT_DIRECTORY}/user.json")
        self.user_payload = json.load(payload)

         # Create an admin user
        admin_user = User(**self.user_payload[0])
        admin_user.set_password(self.user_payload[0].get("password"))
        admin_user.is_staff = True
        admin_user.save()
        self.admin_user = admin_user

        # Create a standard user
        standard_user = User(**self.user_payload[1])
        standard_user.set_password(self.user_payload[1].get("password"))
        standard_user.is_staff = False
        standard_user.save()
        self.standard_user = standard_user

        # Create dummy events
        # Event with higher capacity
        self.event_higher_capacity = Event(**self.event_payload[0])
        self.event_higher_capacity.save()

        # Event with lower capacity
        self.event_lower_capacity = Event(**self.event_payload[1])
        self.event_lower_capacity.save()
    
    def test_create_event_registration(self):
        view = EventRegistrationView.as_view({'post': 'create'})

        # Request with a Low capacity event. Should pass successfully.
        client = APIRequestFactory()
        request = client.post('/api/event_registration/', json.dumps({"event": str(self.event_lower_capacity.pk)}), content_type='application/json')
        force_authenticate(request, user=self.standard_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

        # Duplicate request with Low capacity event. Should fail.
        client = APIRequestFactory()
        request = client.post('/api/event_registration/', json.dumps({"event": str(self.event_lower_capacity.pk)}), content_type='application/json')
        force_authenticate(request, user=self.standard_user)
        response = view(request)
        self.assertEqual(response.status_code, 226)

    def test_event_registration_list(self):
        view = EventRegistrationView.as_view({'get': 'list', 'post': 'create'})

        # Do a new event registration
        client = APIRequestFactory()
        request = client.post('/api/event_registration/', json.dumps({"event": str(self.event_lower_capacity.pk)}), content_type='application/json')
        force_authenticate(request, user=self.standard_user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

        # Make API call to get the event registration data
        client = APIRequestFactory()
        request = client.get(f'/api/event_registration/', content_type='application/json')
        force_authenticate(request, user=self.standard_user)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("count"), 1)

    def test_cancel_event_registration(self):
        view = EventRegistrationView.as_view({'get': 'retrieve', 'delete': 'destroy'})

        # Create a new event reservation
        event_registration_data = {
            "event": self.event_higher_capacity.pk, 
            "booked_by": self.standard_user.pk
        }
        event_registration = EventRegistrationSerializer(data=event_registration_data)
        if event_registration.is_valid():
            event_registration_instance = event_registration.save()
        self.assertEqual(event_registration_instance.event.name, self.event_higher_capacity.name)
        self.assertEqual(event_registration_instance.booked_by.username, self.standard_user.username)

        # Make API call to get the event data
        client = APIRequestFactory()
        request = client.delete(f'/api/event_registration/')
        force_authenticate(request, user=self.standard_user)
        response = view(request, pk=str(event_registration_instance.pk))
        self.assertEqual(response.status_code, 410)

        serialized_event_registration = EventRegistrationSerializer(instance=EventRegistration.objects.get(pk=str(event_registration_instance.pk)), many=False)
        self.assertFalse(serialized_event_registration.data.get("is_active"))