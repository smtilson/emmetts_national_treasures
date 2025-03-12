from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import json
from unittest import skip


User = get_user_model()


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.test_user = User.objects.create_user(
            email="user@example.com", handle="testuser", password="password123"
        )

        self.admin = User.objects.create_user(
            email="admin@example.com",
            handle="adminuser",
            password="password123",
            is_staff=True,
        )

        self.superuser = User.objects.create_superuser(
            email="superuser@example.com", handle="superuser", password="password123"
        )

        # Additional user for list testing
        self.another_user = User.objects.create_user(
            email="another@example.com", handle="anotheruser", password="password123"
        )

        # Set up endpoint URLs
        self.list_url = reverse("user-list")  # Adjust based on your URL name
        self.detail_url = reverse(
            "user-detail", args=[self.another_user.id]
        )  # Adjust based on your URL name

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def authenticate(self, user):
        token = self.get_tokens_for_user(user)["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users cannot access user endpoints"""
        # Clear any authentication
        self.client.credentials()

        # Try to access list endpoint
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try to access detail endpoint
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_users(self):
        """Test authenticated user can list all users"""
        # Authenticate as regular user
        self.authenticate(self.test_user)
        count = User.objects.count()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that all users are returned and ordered by date_joined
        self.assertEqual(len(response.data), count)  # We created 3 users in setup

    def test_retrieve_user(self):
        """Test authenticated user can retrieve user details"""
        self.authenticate(self.test_user)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify user data
        self.assertEqual(response.data["email"], self.another_user.email)
        self.assertEqual(response.data["handle"], self.another_user.handle)

    def test_create_user_not_allowed(self):
        """Test that create method is disabled and returns 405"""
        self.authenticate(self.test_user)

        user_data = {
            "email": "new@example.com",
            "handle": "newuser",
            "password": "newpassword123",
        }

        response = self.client.post(self.list_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Verify the error message
        self.assertIn("Use the signup endpoint instead", response.content.decode())

    def test_update_user(self):
        """Test user can update their own details"""
        self.authenticate(self.test_user)

        # Get URL for the authenticated user
        my_url = reverse("user-detail", args=[self.test_user.id])

        update_data = {
            "handle": "updated_handle",
        }

        response = self.client.patch(my_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the update worked
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.handle, "updated_handle")

    def test_admin_can_update_others(self):
        """Test admin users can update other users"""
        self.authenticate(self.admin)

        update_data = {
            "handle": "admin_updated_handle",
        }

        response = self.client.patch(self.detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the update worked
        self.another_user.refresh_from_db()
        self.assertEqual(self.another_user.handle, "admin_updated_handle")

    def test_user_cannot_update_others(self):
        """Test regular users cannot update other users"""
        self.authenticate(self.test_user)

        update_data = {
            "handle": "hacker_updated_handle",
        }

        # This might return 403 or 404 depending on your permission implementation
        response = self.client.patch(self.detail_url, update_data)
        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
        )

        # Verify no change occurred
        self.another_user.refresh_from_db()
        self.assertEqual(self.another_user.handle, "anotheruser")

    def test_delete_user(self):
        """Test user deletion"""
        self.authenticate(self.admin)

        response = self.client.delete(self.detail_url)

        # Check status code (could be 204 No Content or 200 OK depending on your implementation)
        self.assertIn(
            response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK]
        )

        # Verify user was deleted
        self.assertEqual(User.objects.filter(id=self.another_user.id).count(), 0)


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
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

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
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

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
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

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
        # should I be testing for an error message here
        self.assertIn("email", response.data)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

        # Missing password
        missing_password = {"email": "test@example.com", "handle": "testuser"}
        response = self.client.post(
            self.signup_url,
            data=json.dumps(missing_password),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

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
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

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
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_response_contains_token(self):
        """Test that the response contains a token after successful signup"""
        response = self.client.post(
            self.signup_url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("login")  # Adjust if your URL name is different

        # Create a test user
        self.user_data = {
            "email": "test@example.com",
            "handle": "handle",
            "password": "testpassword123",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_successful_login(self):
        """Test successful login returns tokens and user data with 200 status."""
        response = self.client.post(
            self.login_url, {"email": "test@example.com", "password": "testpassword123"}
        )

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify tokens are present
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Verify user data is present
        self.assertIn("id", response.data)
        self.assertIn("email", response.data)
        self.assertIn("handle", response.data)

        # Verify returned data matches user
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["handle"], self.user_data["handle"])

    def test_invalid_credentials(self):
        """Test login with wrong password returns 401 and error message without tokens."""
        response = self.client.post(
            self.login_url, {"email": "test@example.com", "password": "wrongpassword"}
        )

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify error message
        self.assertIn("detail", response.data)
        self.assertIn(
            "No active account found with the given credentials",
            response.data["detail"],
        )

        # Verify tokens are NOT present
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_nonexistent_user(self):
        """Test login with non-existent user returns 401 and error message."""
        response = self.client.post(
            self.login_url,
            {"email": "nonexistent@example.com", "password": "testpassword123"},
        )

        # Check status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify tokens are NOT present
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_missing_fields(self):
        """Test login with missing fields returns 400 and appropriate errors."""
        # Test missing password
        response1 = self.client.post(self.login_url, {"email": "test@example.com"})
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response1.data)
        self.assertNotIn("access", response1.data)

        # Test missing email
        response2 = self.client.post(self.login_url, {"password": "testpassword123"})
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response2.data)
        self.assertNotIn("access", response2.data)

        # Test empty request
        response3 = self.client.post(self.login_url, {})
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("access", response3.data)

    def test_get_method_returns_message(self):
        """Test GET request to login endpoint returns informational message."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    # Don't worry about rejecting invalid fields right now.
