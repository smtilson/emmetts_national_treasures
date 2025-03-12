from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from unittest import skip
from users.api.serializers import UserSerializer, SignUpSerializer, LoginSerializer


User = get_user_model()


class BaseUserSerializerTests(TestCase):

    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "handle": "testuser",
            "password": "securepassword123",
        }
        self.friend_data = {
            "email": "friend@example.com",
            "handle": "frienduser",
            "password": "password123",
        }

    def add_friend(self):
        self.user.friends.add(self.friend)
        self.user.save()
        self.friend.save()
        self.user.refresh_from_db()
        self.friend.refresh_from_db()


class UserSerializerTests(BaseUserSerializerTests):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(**self.user_data)
        self.friend = User.objects.create_user(**self.friend_data)

        self.serializer = UserSerializer(instance=self.user)

    def test_read_user_serialization(self):
        """Test that a user instance is correctly serialized"""
        # The serializer and user are already set up in BaseUserSerializerTests
        data = self.serializer.data

        # Verify all fields are correctly serialized
        self.assertEqual(data["email"], self.user_data["email"])
        self.assertEqual(data["handle"], self.user_data["handle"])
        self.assertEqual(data["is_active"], True)
        self.assertEqual(data["is_staff"], False)
        self.assertEqual(data["is_superuser"], False)
        self.assertIn("date_joined", data)
        self.assertIn("last_login", data)
        self.assertEqual(len(data["friends"]), 0)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = [
            "id",
            "email",
            "handle",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
            "friends",
        ]
        self.assertEqual(set(data.keys()), set(expected_fields))

    def test_password_field_not_in_serializer_data(self):
        """Test that password is not included in serialized data"""
        data = self.serializer.data
        self.assertNotIn("password", data)

    def test_email_field_content(self):
        """Test that email field content is correct"""
        data = self.serializer.data
        self.assertEqual(data["email"], self.user_data["email"])

    def test_handle_field_content(self):
        """Test that handle field content is correct"""
        data = self.serializer.data
        self.assertEqual(data["handle"], self.user_data["handle"])

    def test_update(self):
        """Test that read-only fields cannot be updated"""
        update_data = {
            "email": "newemail@example.com",
            "handle": "newhandle",
            "id": 10,  # This is a read-only field
            "date_joined": "2022-01-01",  # This is a read-only field
            "is_staff": True,  # This is a read-only field
            "is_active": False,  # This is a read-only field
            "is_superuser": True,  # This is a read-only field
        }
        serializer = UserSerializer(self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        # Check that mutable fields were updated
        self.assertEqual(updated_user.email, "newemail@example.com")
        self.assertEqual(updated_user.handle, "newhandle")

        # Check that read-only fields were not updated
        self.assertFalse(updated_user.id == 10)
        self.assertFalse(updated_user.date_joined == "2022-01-01")
        self.assertFalse(updated_user.is_superuser)
        self.assertFalse(updated_user.is_staff)
        self.assertTrue(updated_user.is_active)

    def test_friends_field_is_empty_by_default(self):
        """Test that a new user has no friends by default"""
        data = self.serializer.data
        self.assertEqual(data["friends"], [])

    def test_friends_field_contains_user_ids(self):
        """Test that friends field contains user IDs when friends are added"""
        self.add_friend()
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data["friends"], [self.friend.id])

    def test_validation_email_format(self):
        """Test that email format is properly validated"""
        # Test with invalid email format
        invalid_data = {
            "email": "invalid-email",  # Not a valid email format
            "handle": "testhandle",
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

        # Test with valid email format
        valid_data = {"email": "valid@example.com", "handle": "testhandle"}
        serializer = UserSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_handle_can_be_empty(self):
        """Test that handle field can be empty or None"""
        # Test updating to empty string
        update_data = {"handle": ""}
        serializer = UserSerializer(self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())

        # Test updating to None
        update_data = {"handle": None}
        serializer = UserSerializer(self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())

        # Save the user with empty handle and verify
        updated_user = serializer.save()
        self.assertIsNone(updated_user.handle)

    def test_handle_uniqueness_validation(self):
        """Test that the serializer validates handle uniqueness"""
        # Creation is handled by the signup serializer
        # Test for case where we try to update an existing user to have a duplicate handle
        update_user = User.objects.create_user(
            email="update@example.com",
            handle="original",
            password="password123",
        )

        update_serializer = UserSerializer(
            instance=update_user,
            data={
                "handle": self.user_data["handle"]
            },  # Try to update to existing handle
            partial=True,
        )

        self.assertFalse(update_serializer.is_valid())
        self.assertIn("handle", update_serializer.errors)

    def test_create_not_implemented(self):
        """Test that UserSerializer cannot be used for user creation"""
        new_data = {
            "email": "newuser@example.com",
            "handle": "newuser",
            "password": "password123",
        }
        serializer = UserSerializer(data=new_data)
        self.assertTrue(serializer.is_valid())  # Data should be valid

        # Attempting to create a user should raise NotImplementedError
        with self.assertRaises(NotImplementedError):
            serializer.save()  # This calls create() internally


class SignUpSerializerTests(BaseUserSerializerTests):
    def setUp(self):
        super().setUp()
        # self.serializer = SignUpSerializer(data=self.user_data)

    def test_valid_signup_with_all_fields(self):
        """Test creating a user with all fields provided"""
        serializer = SignUpSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.handle, self.user_data["handle"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_signup_without_handle(self):
        """Test creating a user without a handle (which is optional)"""
        self.user_data.pop("handle")
        serializer = SignUpSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, self.user_data["email"])
        self.assertIsNone(user.handle)

    def test_handle_uniqueness_validation(self):
        """Test that the serializer validates handle uniqueness"""
        # Create an existing user with a handle
        User.objects.create_user(**self.user_data)
        # Now try to create another user with the same handle via serializer
        duplicate_data = {
            "email": "new@example.com",
            "handle": self.user_data["handle"],  # Same handle as existing user
            "password": "password456",
        }

        serializer = UserSerializer(data=duplicate_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("handle", serializer.errors)

    def test_password_validation(self):
        """Test that password validation is applied"""
        # Test with a simple password that should fail validation
        data = {
            "email": "user@example.com",
            "handle": "testhandle",
            "password": "password",  # Too simple
        }
        serializer = SignUpSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_password_is_hashed(self):
        """Test that password is properly hashed when stored"""
        serializer = SignUpSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Password should not be stored in plaintext
        self.assertNotEqual(user.password, self.user_data["password"])
        # But it should validate correctly
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_password_not_in_serialized_output(self):
        """Test that password is not included in serialized output"""
        serializer = SignUpSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        # Serialize the created user
        result_serializer = SignUpSerializer(user)
        self.assertNotIn("password", result_serializer.data)

    def test_email_format_validation(self):
        """Test that email format is properly validated"""
        data = {
            "email": "not-an-email",  # Invalid email format
            "handle": "testhandle",
            "password": "SecurePassword123!",
        }
        serializer = SignUpSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_email_required(self):
        """Test that email is required"""
        data = {"handle": "testhandle", "password": "SecurePassword123!"}
        serializer = SignUpSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_password_required(self):
        """Test that password is required"""
        data = {"email": "user@example.com", "handle": "testhandle"}
        serializer = SignUpSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_update_not_implemented(self):
        """Test that SignUpSerializer cannot be used for user updates"""
        # First create a user
        user = User.objects.create_user(**self.user_data)

        # Try to update the user with SignUpSerializer
        update_data = {"handle": "updated_handle"}

        serializer = SignUpSerializer(instance=user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())  # Data should be valid

        # Attempting to update should raise NotImplementedError
        with self.assertRaises(NotImplementedError):
            serializer.save()  # This calls update() internally since we provided an instance


class LoginSerializerTests(BaseUserSerializerTests):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(**self.user_data)
        self.login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }

    def test_valid_login(self):
        """Test login with valid credentials returns user"""
        serializer = LoginSerializer(data=self.login_data, context={"request": None})
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertIn("id", validated_data)
        self.assertIn("refresh", validated_data)
        self.assertIn("access", validated_data)
        self.assertIn("handle", validated_data)
        self.assertEqual(validated_data["email"], self.login_data["email"])

    def test_invalid_password(self):
        """Test login with invalid password raises AuthenticationFailed"""
        invalid_data = {"email": self.user_data["email"], "password": "wrongpassword"}
        serializer = LoginSerializer(data=invalid_data, context={"request": None})
        with self.assertRaises(AuthenticationFailed) as e:
            valid = serializer.is_valid()
            self.assertFalse(valid)
            # is this misleading? the error message involves email as well.
            for term in {"password", "invalid"}:
                self.assertIn(term, str(e.exception))

    def test_invalid_email(self):
        """Test login with an invalid email raises AuthenticationFailed"""
        invalid_data = {"email": "nonexistent@example.com", "password": "somepassword"}
        serializer = LoginSerializer(data=invalid_data, context={"request": None})
        with self.assertRaises(AuthenticationFailed) as e:
            valid = serializer.is_valid()
            self.assertFalse(valid)
            for term in {"email", "invalid"}:
                self.assertIn(term, str(e.exception))

    def test_missing_email(self):
        """Test login with missing email raises ValidationError"""
        invalid_data = {"password": self.user_data["password"]}
        serializer = LoginSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as e:
            serializer.is_valid(raise_exception=True)
            print(e.exception)

    def test_missing_password(self):
        """Test login with missing password raises ValidationError"""
        invalid_data = {"email": self.user_data["email"]}
        serializer = LoginSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as e:
            serializer.is_valid(raise_exception=True)
            print(e.exception)

    def test_password_not_in_response(self):
        """Test that password is not included in serialized output"""
        serializer = LoginSerializer(data=self.login_data, context={"request": None})
        self.assertTrue(serializer.is_valid())
        self.assertNotIn("password", serializer.data)
