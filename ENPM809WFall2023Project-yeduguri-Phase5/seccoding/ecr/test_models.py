from django.test import TestCase
from ecr.models import Incident, User, Officer

class IncidentModelTest(TestCase):
    def test_create_incident(self):
        # Create a sample incident
        incident = Incident.objects.create(
            name="John Doe",
            type="Robbery",
            email="john@example.com",
            phone_number="123-456-7890",
            incident_spot="123 Main St",
            zip=12345,
            date="2023-10-09",
            time="14:30:00",
            victim_details="Description of victim",
            culprit_details="Description of culprit",
            status="received",
        )

        # Check if the incident was created successfully
        self.assertEqual(incident.name, "John Doe")
        self.assertEqual(incident.type, "Robbery")

    def test_incident_str_representation(self):
        # Create a sample incident
        incident = Incident.objects.create(name="Alice", type="Burglary")
        self.assertEqual(str(incident), "Incident: Alice (Burglary)")

class UserModelTest(TestCase):
    def test_create_user(self):
        # Create a sample user
        user = User.objects.create(
            name="Alice",
            email="alice@example.com",
            phone_number="987-654-3210",
            address="456 Elm St",
            zip=54321,
        )

        # Check if the user was created successfully
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.email, "alice@example.com")

class OfficerModelTest(TestCase):
    def test_create_officer(self):
        # Create a sample officer
        officer = Officer.objects.create(
            officer_id=1234,
            name="Officer Smith",
            zip=54321,
        )

        # Check if the officer was created successfully
        self.assertEqual(officer.officer_id, 1234)
        self.assertEqual(officer.name, "Officer Smith")
