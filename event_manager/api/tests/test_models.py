import json
from django.contrib.auth.models import User
from django.test import TestCase
from django.db.utils import IntegrityError

from api.models import Event
from api.serializers import EventRegistrationSerializer

TEST_CONTENT_DIRECTORY = "api/tests/test_elements"
TEST_USER_CONTENT_DIRECTORY = "authentication/tests/test_elements"


class TestEventModel(TestCase):
    """This is the test suite for Event"""

    def setUp(self) -> None:
        payload = open(f"{TEST_CONTENT_DIRECTORY}/event_payload.json")
        self.payload = json.load(payload)

    def test_all_records_are_successfully_created(self):
        events = []
        for event_data in self.payload:
            event = Event(**event_data)
            event.save()
            events.append(event)

        for index, instance in enumerate(events):
            self.assertEqual(instance.name, self.payload[index]["name"])

    def test_duplicate_records_should_fail(self):
        """
        We're trying to save two records with the same username, which should fail.
        """
        event = Event(**self.payload[0])
        event.save()
        # Now we're attempting to create a duplicate record 
        event = Event(**self.payload[0])
        self.assertRaises(IntegrityError, event.save)

class TestEventRegistrationModel(TestCase):
    """This is the test suite for Event Registration"""

    def setUp(self) -> None:
        event_payload = open(f"{TEST_CONTENT_DIRECTORY}/event_payload.json")
        self.event_payload = json.load(event_payload)

        user_payload = open(f"{TEST_USER_CONTENT_DIRECTORY}/user.json")
        self.user_payload = json.load(user_payload)

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

        # Create events
        # Event with higher capacity
        self.event_higher_capacity = Event(**self.event_payload[0])
        self.event_higher_capacity.save()

        # Event with lower capacity
        self.event_lower_capacity = Event(**self.event_payload[1])
        self.event_lower_capacity.save()

    def test_event_registration_successfully_created(self):
        event_registration_data = {
            "event": self.event_higher_capacity.pk, 
            "booked_by": self.standard_user.pk
        }
        event_registration = EventRegistrationSerializer(data=event_registration_data)
        if event_registration.is_valid():
            event_registration_instance = event_registration.save()
        self.assertEqual(event_registration_instance.event.name, self.event_higher_capacity.name)
        self.assertEqual(event_registration_instance.booked_by.username, self.standard_user.username)


    def test_malformed_supplier_payload(self):
        """
        We have provided incomplete data in the payload and it is
        expected to return False in case of serializer is_valid test.
        """
        event_registration_data = {
            "event": self.event_higher_capacity.pk, 
        }
        event_registration = EventRegistrationSerializer(data=event_registration_data)
        self.assertFalse(event_registration.is_valid())

