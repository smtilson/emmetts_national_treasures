from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from ..models import CustomUser


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "handle": "testuserhandle",
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_create_user(self):
        from django.test import TestCase


from django.db import IntegrityError
from django.core.exceptions import ValidationError

from ..models import CustomUser


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "handle": "testuserhandle",
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Test creating a basic user with required fields"""
        new_user = CustomUser.objects.create_user(
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
        db_user = CustomUser.objects.get(email="newuser@example.com")
        self.assertEqual(db_user.id, new_user.id)

    def test_create_user_without_handle(self):
        """Test creating a user without a handle (which is allowed)"""
        user = CustomUser.objects.create_user(
            email="nohandle@example.com", password="password123"
        )
        self.assertEqual(user.email, "nohandle@example.com")
        self.assertEqual(user.handle, "")

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpass123", handle="admin"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_email_uniqueness(self):
        """Test that email must be unique"""
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email="test@example.com",  # Same as self.user
                password="different123",
                handle="different",
            )

    def test_handle_uniqueness(self):
        """Test that handle must be unique if provided"""
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email="different@example.com",
                password="different123",
                handle="testuserhandle",  # Same as self.user
            )

    def test_user_str_representation(self):
        """Test the string representation of a user"""
        self.assertEqual(str(self.user), "testuserhandle")

    def test_read_user(self):
        """Test retrieving a user"""
        retrieved_user = CustomUser.objects.get(email="test@example.com")
        self.assertEqual(retrieved_user.handle, "testuserhandle")
        self.assertEqual(retrieved_user, self.user)

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
        user_to_delete = CustomUser.objects.create_user(
            email="delete_me@example.com", password="delete123", handle="delete_me"
        )
        user_id = user_to_delete.id
        user_to_delete.delete()

        # Verify the user no longer exists
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=user_id)

    def test_dummy_user_creation(self):
        """Test creating a dummy user"""
        initial_count = CustomUser.dummy_count()
        dummy = CustomUser.dummy_user()

        # Check the dummy user was created correctly
        self.assertEqual(dummy.handle, f"dummy_{initial_count}")
        self.assertEqual(dummy.email, f"dummy{initial_count}@example.com")

        # Check the count increased
        self.assertEqual(CustomUser.dummy_count(), initial_count + 1)

    def test_dummy_count(self):
        """Test counting dummy users"""
        initial_count = CustomUser.dummy_count()

        # Create some dummy users and non-dummy users
        CustomUser.objects.create_user(
            email="dummy_test1@example.com", password="password", handle="dummy_test1"
        )
        CustomUser.objects.create_user(
            email="not_dummy@example.com", password="password", handle="regular_user"
        )
        CustomUser.objects.create_user(
            email="dummy_test2@example.com", password="password", handle="dummy_test2"
        )

        # Only users with handles starting with "dummy" should be counted
        expected_count = initial_count + 2  # Only the dummy_* handles
        self.assertEqual(CustomUser.dummy_count(), expected_count)

    def test_cannot_create_user_without_email(self):
        """Test that email is required to create a user"""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="", password="password123", handle="no_email"
            )

    def test_inactive_user(self):
        """Test creating an inactive user"""
        inactive_user = CustomUser.objects.create_user(
            email="inactive@example.com",
            password="inactive123",
            handle="inactive",
            is_active=False,
        )
        self.assertFalse(inactive_user.is_active)

        """Test creating a basic user with required fields"""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.handle, "testuserhandle")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.check_password("testpassword123"))

    def test_create_user_without_handle(self):
        """Test creating a user without a handle (which is allowed)"""
        user = CustomUser.objects.create_user(
            email="nohandle@example.com", password="password123"
        )
        self.assertEqual(user.email, "nohandle@example.com")
        self.assertEqual(user.handle, "")

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpass123", handle="admin"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_email_uniqueness(self):
        """Test that email must be unique"""
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email="test@example.com",  # Same as self.user
                password="different123",
                handle="different",
            )

    def test_handle_uniqueness(self):
        """Test that handle must be unique if provided"""
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email="different@example.com",
                password="different123",
                handle="testuserhandle",  # Same as self.user
            )

    def test_user_str_representation(self):
        """Test the string representation of a user"""
        self.assertEqual(str(self.user), "testuserhandle")

    def test_read_user(self):
        """Test retrieving a user"""
        retrieved_user = CustomUser.objects.get(email="test@example.com")
        self.assertEqual(retrieved_user.handle, "testuserhandle")
        self.assertEqual(retrieved_user, self.user)

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
        user_to_delete = CustomUser.objects.create_user(
            email="delete_me@example.com", password="delete123", handle="delete_me"
        )
        user_id = user_to_delete.id
        user_to_delete.delete()

        # Verify the user no longer exists
        with self.assertRaises(CustomUser.DoesNotExist):
            CustomUser.objects.get(id=user_id)

    def test_dummy_user_creation(self):
        """Test creating a dummy user"""
        initial_count = CustomUser.dummy_count()
        dummy = CustomUser.dummy_user()

        # Check the dummy user was created correctly
        self.assertEqual(dummy.handle, f"dummy_{initial_count}")
        self.assertEqual(dummy.email, f"dummy{initial_count}@example.com")

        # Check the count increased
        self.assertEqual(CustomUser.dummy_count(), initial_count + 1)

    def test_dummy_count(self):
        """Test counting dummy users"""
        initial_count = CustomUser.dummy_count()

        # Create some dummy users and non-dummy users
        CustomUser.objects.create_user(
            email="dummy_test1@example.com", password="password", handle="dummy_test1"
        )
        CustomUser.objects.create_user(
            email="not_dummy@example.com", password="password", handle="regular_user"
        )
        CustomUser.objects.create_user(
            email="dummy_test2@example.com", password="password", handle="dummy_test2"
        )

        # Only users with handles starting with "dummy" should be counted
        expected_count = initial_count + 2  # Only the dummy_* handles
        self.assertEqual(CustomUser.dummy_count(), expected_count)

    def test_cannot_create_user_without_email(self):
        """Test that email is required to create a user"""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="", password="password123", handle="no_email"
            )

    def test_inactive_user(self):
        """Test creating an inactive user"""
        inactive_user = CustomUser.objects.create_user(
            email="inactive@example.com",
            password="inactive123",
            handle="inactive",
            is_active=False,
        )
        self.assertFalse(inactive_user.is_active)
