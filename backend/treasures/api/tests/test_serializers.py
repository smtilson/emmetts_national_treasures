from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from treasures.models import Treasure
from treasures.api.serializers import TreasureSerializer

User = get_user_model()


class TreasureSerializerTest(TestCase):
    def setUp(self):
        # Create test user
        self.user_data = {
            "email": "test@example.com",
            "handle": "testuser",
            "password": "testpass123",
        }
        self.user = User.objects.create_user(**self.user_data)

        # Create test treasure
        self.treasure_data = {
            "name": "Test Treasure",
            "category": "Test Category",
            "description": "This is a test description for serializer testing.",
        }
        self.treasure = Treasure.objects.create(creator=self.user, **self.treasure_data)
        self.treasure_data["id"] = self.treasure.id
        self.treasure_data["date_added"] = self.treasure.date_added
        self.treasure_data["last_modified"] = self.treasure.last_modified
        self.treasure_data["short_details"] = self.treasure.short_details
        self.treasure_data["truncated_description"] = self.treasure.truncated
        # Create serializer instance
        self.serializer = TreasureSerializer(instance=self.treasure)

    def test_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        data = self.serializer.data
        expected_fields = [
            "id",
            "creator",
            "creator_handle",
            "name",
            "category",
            "description",
            "date_added",
            "last_modified",
            "short_details",
            "truncated_description",
        ]

        self.assertEqual(set(data.keys()), set(expected_fields))

    def test_serialized_field_values(self):
        """Test that all fields are correctly serialized with expected values"""
        data = self.serializer.data

        # Basic fields
        self.assertEqual(data["id"], self.treasure.id)
        self.assertEqual(data["name"], self.treasure_data["name"])
        self.assertEqual(data["category"], self.treasure_data["category"])
        self.assertEqual(data["description"], self.treasure_data["description"])

        # Relationship fields
        self.assertEqual(data["creator"], self.user.id)  # Should be the PK of the user
        self.assertEqual(data["creator_handle"], self.user.handle)

        # Auto-generated fields
        # For date fields, we'll just verify they exist and are not None
        self.assertIsNotNone(data["date_added"])
        self.assertIsNotNone(data["last_modified"])

        # Method fields
        self.assertEqual(data["short_details"], self.treasure.short_details)
        self.assertEqual(data["truncated_description"], self.treasure.truncated)

    def test_update_respects_read_only_fields(self):
        """Test that updates only affect writable fields and respect read-only fields"""
        # Create a new user to try to change creator
        another_user = User.objects.create_user(
            email="another@example.com", handle="anotheruser", password="testpass123"
        )

        # Attempt to update all fields, including read-only ones
        update_data = {
            "id": 99999,  # Should be ignored (not explicitly in serializer but implicitly read-only)
            "name": "Updated Name",
            "category": "Updated Category",
            "description": "Updated description for testing read-only field handling.",
            "creator": another_user.id,  # Should be ignored (read-only)
            "creator_handle": "attempt_to_change",  # Should be ignored (method field)
            "date_added": "2020-01-01T00:00:00Z",  # Should be ignored (read-only)
            "last_modified": "2020-01-01T00:00:00Z",  # Should be ignored (read-only)
            "short_details": "attempt_to_change",  # Should be ignored (method field)
            "truncated_description": "attempt_to_change",  # Should be ignored (method field)
        }

        serializer = TreasureSerializer(
            instance=self.treasure, data=update_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        updated_treasure = serializer.save()

        # Refresh from database to ensure we're seeing saved changes
        updated_treasure.refresh_from_db()

        # Check writable fields - SHOULD be updated
        self.assertEqual(updated_treasure.name, "Updated Name")
        self.assertEqual(updated_treasure.category, "Updated Category")
        self.assertEqual(
            updated_treasure.description,
            "Updated description for testing read-only field handling.",
        )

        # Check read-only fields - should NOT be updated
        self.assertEqual(updated_treasure.id, self.treasure_data["id"])
        self.assertEqual(updated_treasure.creator, self.user)
        self.assertEqual(updated_treasure.date_added, self.treasure_data["date_added"])

        # last_modified is a special case - it should be updated automatically because of auto_now=True
        # but not to our specified value
        self.assertNotEqual(
            updated_treasure.last_modified, self.treasure_data["last_modified"]
        )  # Should be changed
        self.assertNotEqual(
            updated_treasure.last_modified.isoformat(), "2020-01-01T00:00:00+00:00"
        )  # But not to our value

        # Check computed properties - should reflect the new values of the underlying fields
        expected_new_short_details = (
            f"Updated Name - Updated Category by {self.user.handle}"
        )
        self.assertEqual(updated_treasure.short_details, expected_new_short_details)

        # For truncated_description
        self.assertIn(update_data["name"], updated_treasure.truncated)
        self.assertIn(self.user.handle, updated_treasure.truncated)
        self.assertIn(update_data["description"][:50], updated_treasure.truncated)
        if len(update_data["description"]) > 50:
            self.assertIn("...", updated_treasure.truncated)

    def test_validate_name_not_blank(self):
        """Test that name validation rejects blank names"""
        # Test with blank name
        data = {"name": "   "}  # Just spaces
        serializer = TreasureSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_unknown_field_rejection(self):
        """Test that unknown fields are rejected based on BaseSerializerMixin"""
        data = {"name": "Valid Name", "unknown_field": "This should cause an error"}

        serializer = TreasureSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create_treasure(self):
        """Test that serializer can create a treasure"""
        data = {
            "name": "New Treasure",
            "category": "New Category",
            "description": "New description",
        }

        serializer = TreasureSerializer(
            data=data, context={"request": type("obj", (object,), {"user": self.user})}
        )
        serializer.is_valid(raise_exception=True)

        # Note: This might need adjustment based on how you handle creator assignment
        # in your views. For testing, we're providing user in the context.
        treasure = serializer.save(creator=self.user)

        self.assertEqual(treasure.name, "New Treasure")
        self.assertEqual(treasure.category, "New Category")
        self.assertEqual(treasure.description, "New description")
        self.assertEqual(treasure.creator, self.user)

    def test_partial_update(self):
        """Test that serializer can partially update a treasure"""
        data = {"name": "Partial Update"}

        serializer = TreasureSerializer(instance=self.treasure, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_treasure = serializer.save()

        # Check that specified field was updated
        self.assertEqual(updated_treasure.name, "Partial Update")

        # Check that other fields were not changed
        self.assertEqual(updated_treasure.category, "Test Category")
        self.assertEqual(
            updated_treasure.description,
            "This is a test description for serializer testing.",
        )

    def test_creator_handle_field(self):
        """Test that creator_handle method field returns correct value"""
        data = self.serializer.data
        self.assertEqual(data["creator_handle"], "testuser")

    def test_short_details_field(self):
        """Test that short_details method field returns correct value"""
        data = self.serializer.data
        # This should match the model's short_details property implementation
        expected = "Test Treasure - Test Category by testuser"
        self.assertEqual(data["short_details"], expected)

    def test_readonly_fields(self):
        """Test that read-only fields are not writable"""
        data = {
            "name": "Updated Name",
            "category": "Updated Category",
            "description": "Updated description",
            "creator": 999,  # Should be ignored as read-only
            "date_added": "2023-01-01T00:00:00Z",  # Should be ignored as read-only
            "last_modified": "2023-01-01T00:00:00Z",  # Should be ignored as read-only
        }

        serializer = TreasureSerializer(instance=self.treasure, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_treasure = serializer.save()

        # Check that writable fields were updated
        self.assertEqual(updated_treasure.name, "Updated Name")
        self.assertEqual(updated_treasure.category, "Updated Category")
        self.assertEqual(updated_treasure.description, "Updated description")

        # Check that read-only fields were not changed
        self.assertEqual(updated_treasure.creator.id, self.user.id)

    def test_validate_name_not_blank(self):
        """Test that name validation rejects blank names"""
        # Test with blank name
        data = {"name": "   "}  # Just spaces
        serializer = TreasureSerializer(data=data)

        with self.assertRaises(ValidationError) as e:
            serializer.is_valid(raise_exception=True)
            print()
            print(e)
            print()

    def test_unknown_field_rejection(self):
        """Test that unknown fields are rejected based on BaseSerializerMixin"""
        data = {"name": "Valid Name", "unknown_field": "This should cause an error"}

        serializer = TreasureSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create_treasure(self):
        """Test that serializer can create a treasure"""
        data = {
            "name": "New Treasure",
            "category": "New Category",
            "description": "New description",
        }

        serializer = TreasureSerializer(
            data=data, context={"request": type("obj", (object,), {"user": self.user})}
        )
        serializer.is_valid(raise_exception=True)

        # Note: This might need adjustment based on how you handle creator assignment
        # in your views. For testing, we're providing user in the context.
        treasure = serializer.save(creator=self.user)

        self.assertEqual(treasure.name, "New Treasure")
        self.assertEqual(treasure.category, "New Category")
        self.assertEqual(treasure.description, "New description")
        self.assertEqual(treasure.creator, self.user)

    def test_partial_update(self):
        """Test that serializer can partially update a treasure"""
        data = {"name": "Partial Update"}

        serializer = TreasureSerializer(instance=self.treasure, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_treasure = serializer.save()

        # Check that specified field was updated
        self.assertEqual(updated_treasure.name, "Partial Update")

        # Check that other fields were not changed
        self.assertEqual(updated_treasure.category, "Test Category")
        self.assertEqual(
            updated_treasure.description,
            "This is a test description for serializer testing.",
        )
