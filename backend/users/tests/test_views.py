from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import json
from unittest import skip

User = get_user_model()



class SignupViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("signup")  # Make sure this matches your URL name
        self.valid_payload = {
            "email": "test@example.com",
            "handle": "testuser",
            "password": "securepassword123",
        }
        self.minimal_payload = {
            "email": "minimal@example.com",
            "password": "securepassword123",
        }

    def test_get_signup_view(self):
        """Test that GET request returns help message"""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_create_user_valid_data(self):
        """Test creating a user with valid data"""
        response = self.client.post(
            self.signup_url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that user was created in database
        self.assertTrue(User.objects.filter(email=self.valid_payload["email"]).exists())

        # Check response data
        self.assertEqual(response.data["email"], self.valid_payload["email"])
        self.assertEqual(response.data["handle"], self.valid_payload["handle"])
        self.assertNotIn("password", response.data)  # Password should not be returned

    def test_create_user_without_handle(self):
        """Test creating a user without handle (which is optional)"""
        response = self.client.post(
            self.signup_url,
            data=json.dumps(self.minimal_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that user was created in database
        user = User.objects.get(email=self.minimal_payload["email"])
        self.assertIsNone(user.handle)

    def test_password_is_hashed(self):
        """Test that password is properly hashed"""
        self.client.post(
            self.signup_url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        user = User.objects.get(email=self.valid_payload["email"])
        self.assertNotEqual(user.password, self.valid_payload["password"])
        self.assertTrue(user.check_password(self.valid_payload["password"]))

    def test_create_user_invalid_email(self):
        """Test creating a user with invalid email format"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = "not-an-email"

        response = self.client.post(
            self.signup_url,
            data=json.dumps(invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_user_missing_required_fields(self):
        """Test creating a user with missing required fields"""
        # Missing email
        missing_email = {"handle": "testuser", "password": "securepassword123"}
        response = self.client.post(
            self.signup_url,
            data=json.dumps(missing_email),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

        # Missing password
        missing_password = {"email": "test@example.com", "handle": "testuser"}
        response = self.client.post(
            self.signup_url,
            data=json.dumps(missing_password),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_create_duplicate_email(self):
        """Test creating a user with an email that already exists"""
        # Create a user first
        self.client.post(
            self.signup_url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        # Try to create another user with the same email
        duplicate_email = {
            "email": self.valid_payload["email"],
            "handle": "different",
            "password": "differentpassword123",
        }

        response = self.client.post(
            self.signup_url,
            data=json.dumps(duplicate_email),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_duplicate_handle(self):
        """Test creating a user with a handle that already exists"""
        # Create a user first
        self.client.post(
            self.signup_url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        # Try to create another user with the same handle
        duplicate_handle = {
            "email": "different@example.com",
            "handle": self.valid_payload["handle"],
            "password": "differentpassword123",
        }

        response = self.client.post(
            self.signup_url,
            data=json.dumps(duplicate_handle),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("handle", response.data)

    @skip
    def test_response_contains_token(self):
        """Test that the response contains a token after successful signup"""
        response = self.client.post(
            self.signup_url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertIsNotNone(response.data["token"])
