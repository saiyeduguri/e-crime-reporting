from django.test import TestCase
from ecr.models import Incident, User, Officer
from django.test import TestCase
from django.urls import reverse

class IncidentModelTest(TestCase):
    def test_create_incident_with_valid_data(self):
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
        self.assertEqual(incident.name, "John Doe")
        self.assertEqual(incident.type, "Robbery")

    def test_create_incident_with_invalid_data(self):
        # Attempt to create an incident with missing required fields
        with self.assertRaises(Exception):
            Incident.objects.create(
                name="Alice",
                type="Burglary"
            )

class UserModelTest(TestCase):
    def test_create_user_with_valid_data(self):
        user = User.objects.create(
            name="Alice",
            email="alice@example.com",
            phone_number="987-654-3210",
            address="456 Elm St",
            zip=54321,
        )
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.email, "alice@example.com")

    def test_create_user_with_invalid_data(self):
        # Attempt to create a user with missing required fields
        with self.assertRaises(Exception):
            User.objects.create(
                name="John",
                email="john@example.com"
            )

class OfficerModelTest(TestCase):
    def test_create_officer_with_valid_data(self):
        officer = Officer.objects.create(
            officer_id=1234,
            name="Officer Smith",
            zip=54321,
        )
        self.assertEqual(officer.officer_id, 1234)
        self.assertEqual(officer.name, "Officer Smith")

    def test_create_officer_with_invalid_data(self):
        # Attempt to create an officer with missing required fields
        with self.assertRaises(Exception):
            Officer.objects.create(
                officer_id=5678,
                name="Officer Johnson"
            )
class RedirectionTest(TestCase):
    def test_user_login_redirect(self):
        response = self.client.get(reverse('user_login'))
        self.assertEqual(response.status_code, 200)

    def test_officer_login_redirect(self):
        response = self.client.get(reverse('officer_login'))
        self.assertEqual(response.status_code, 200)

    def test_user_home_redirect(self):
        response = self.client.get(reverse('user_home'))
        self.assertEqual(response.status_code, 200)

    def test_user_report_incident_redirect(self):
        response = self.client.get(reverse('user_report_incident'))
        self.assertEqual(response.status_code, 200)

    def test_user_check_status_redirect(self):
        response = self.client.get(reverse('user_check_status'))
        self.assertEqual(response.status_code, 302)

    def test_user_check_crime_rate_redirect(self):
        response = self.client.get(reverse('user_check_crime_rate'))
        self.assertEqual(response.status_code, 200)

    def test_officer_home_redirect(self):
        response = self.client.get(reverse('officer_home'))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirect(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)



from django.urls import reverse

class UserRegistrationHTMLTest(TestCase):
    def test_user_registration_page(self):
       
        url = reverse('user_registration')
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the HTML content contains expected elements
        self.assertContains(response, '<h1>User Registration</h1>', html=True)
        self.assertContains(response, 'Name:', html=True)
        self.assertContains(response, 'Driving License or Real ID:', html=True)
        self.assertContains(response, 'Email:', html=True)
        self.assertContains(response, 'Phone Number:', html=True)
        self.assertContains(response, 'Address:', html=True)
        self.assertContains(response, 'Zip Code:', html=True)
        self.assertContains(response, 'Password:', html=True)
        self.assertContains(response, 'Confirm Password:', html=True)

    def test_user_registration_form_fields(self):
       
        url = reverse('user_registration')
        response = self.client.get(url)

        self.assertContains(response, '<input class="form-field required" type="text" id="name" name="name" required>', html=True)
        self.assertContains(response, '<input class="form-field required" type="text" id="id" name="id" required>', html=True)
        self.assertContains(response, '<input class="form-field required" type="email" id="email" name="email" required>', html=True)
        self.assertContains(response, '<input class="form-field required" type="tel" id="phone_number" name="phone_number" pattern="[0-9]{10}" title="Enter a 10-digit phone number" required>', html=True)
        self.assertContains(response, '<input class="form-field required" type="text" id="address" name="address" required>', html=True)
        self.assertContains(response, '<input class="form-field required" type="text" id="zip" name="zip" pattern="\\d{5}" title="Enter a 5-digit zip code" required>', html=True)
        self.assertContains(response, '<input class="form-field required" type="password" id="password" name="password" required>', html=True)
        self.assertContains(response, '<input class="form-field required" type="password" id="confirm_password" name="confirm_password" required>', html=True)


class LoginTestCase(TestCase):
    def test_login_form_elements(self):
        response = self.client.get(reverse('officer_login')) 
        # Check if the form contains the necessary elements
        self.assertContains(response, '<label for="officer_id">Your ID:</label>')
        self.assertContains(response, '<input type="text" id="officer_id" name="officer_id"')
        self.assertContains(response, '<label for="password">Password:</label>')
        self.assertContains(response, '<input type="password" id="password" name="password"')
        self.assertContains(response, '<input type="submit" class="login-button" value="Login">')

    def test_login_form_submission_valid(self):
        response = self.client.post(reverse('officer_login'), {'officer_id': '1', 'password': '123'})  
        # Check if the form is submitted successfully
        self.assertEqual(response.status_code, 302)  

    def test_login_form_submission_invalid(self):
        response = self.client.post(reverse('officer_login'), {'officer_id': '1', 'password': ''})  


    