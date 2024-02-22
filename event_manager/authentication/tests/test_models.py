import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

TEST_CONTENT_DIRECTORY = "authentication/tests/test_elements"


class TestUserModel(TestCase):
    """This is the test suite for User"""

    def setUp(self) -> None:
        payload = open(f"{TEST_CONTENT_DIRECTORY}/user.json")
        self.payload = json.load(payload)

    def test_all_records_are_successfully_created(self):
        users = []
        for user_data in self.payload:
            user = User(**user_data)
            user.save()
            users.append(user)

        for index, instance in enumerate(users):
            self.assertEqual(instance.username, self.payload[index]["username"])

    def test_malformed_supplier_payload(self):
        """
        We're trying to save two records with the same username, which should fail.
        """
        user = User(**self.payload[0])
        user.save()
        # Now 
        user = User(**self.payload[0])
        self.assertRaises(IntegrityError, user.save)
