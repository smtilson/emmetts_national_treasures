from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from unittest import skip
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "handle": "testuserhandle",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Test creating a basic user with required fields"""
        new_user = User.objects.create_user(
            email="newuser@example.com", password="newpassword123", handle="newuser"
        )

        # Assert the user was created with expected attributes
        self.assertEqual(new_user.email, "newuser@example.com")
        self.assertEqual(new_user.handle, "newuser")
        self.assertTrue(new_user.is_active)
        self.assertFalse(new_user.is_staff)
        self.assertTrue(new_user.check_password("newpassword123"))

        # Verify it was actually saved to the database
        self.assertIsNotNone(new_user.pk)
        db_user = User.objects.get(email="newuser@example.com")
        self.assertEqual(db_user.id, new_user.id)

    def test_create_user_without_handle(self):
        """Test creating a user without a handle (which is allowed)"""
        user = User.objects.create_user(
            email="nohandle@example.com", password="password123"
        )
        self.assertEqual(user.email, "nohandle@example.com")
        self.assertEqual(user.handle, None)

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123", handle="admin"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_email_uniqueness(self):
        """Test that email must be unique"""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="test@example.com",  # Same as self.user
                password="different123",
                handle="different",
            )

    def test_email_format_validation(self):
        """Test that emails must be in a valid format"""
        with self.assertRaises(ValidationError):
            user = User(
                email="not-an-email-format",
                password="password123",
                handle="invalidmail",
            )
            user.full_clean()  # This triggers validation

    def test_handle_uniqueness(self):
        """Test that handle must be unique if provided"""
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="different@example.com",
                password="different123",
                handle="testuserhandle",  # Same as self.user
            )

    def test_multiple_users_without_handle(self):
        """Test creating multiple users without handles"""
        # Create 2 users without handles
        user1 = User.objects.create_user(
            email="nohandle1@example.com", password="password123"
        )
        self.assertEqual(user1.handle, None)

        user2 = User.objects.create_user(
            email="nohandle2@example.com", password="password456"
        )
        self.assertEqual(user2.handle, None)
        # If we got here, multiple blank handles are allowed
        # (This is what should happen based on your model definition)
        # Based on Django's behavior with blank=True and unique=True,
        # multiple empty strings should be allowed

        # Verify we have two users with empty handles
        blank_handle_count = User.objects.filter(handle=None).count()
        self.assertEqual(blank_handle_count, 2)

    def test_read_user(self):
        """Test retrieving a user"""
        retrieved_user = User.objects.get(email="test@example.com")
        self.assertEqual(retrieved_user.handle, "testuserhandle")
        self.assertEqual(retrieved_user, self.user)

    def test_user_str_representation(self):
        """Test the string representation of a user with and without handle"""
        # Test user with handle (created in setUp)
        self.assertEqual(str(self.user), "testuserhandle")

        # Test user without handle
        user_without_handle = User.objects.create_user(
            email="nohandle@example.com", password="password123"
        )
        # Should return the part of email before @
        self.assertEqual(str(user_without_handle), "nohandle")

    def test_update_user(self):
        """Test updating user fields"""
        self.user.handle = "updated_handle"
        self.user.is_staff = True
        self.user.save()

        # Refresh from db to ensure changes were saved
        self.user.refresh_from_db()
        self.assertEqual(self.user.handle, "updated_handle")
        self.assertTrue(self.user.is_staff)

    def test_delete_user(self):
        """Test deleting a user"""
        user_to_delete = User.objects.create_user(
            email="delete_me@example.com", password="delete123", handle="delete_me"
        )
        user_id = user_to_delete.id
        user_to_delete.delete()

        # Verify the user no longer exists
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)

    def test_cannot_create_user_without_email(self):
        """Test that email is required to create a user"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="", password="password123", handle="no_email"
            )
