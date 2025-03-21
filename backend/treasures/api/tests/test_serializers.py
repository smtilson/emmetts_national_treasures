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

    def test_create_treasure(self):
        """Test that serializer can create a treasure"""
        data = {
            "name": "New Treasure",
            "category": "New Category",
            "description": "New description",
        }

        serializer = TreasureSerializer(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        treasure = serializer.save(creator=self.user)

        self.assertEqual(treasure.name, "New Treasure")
        self.assertEqual(treasure.category, "New Category")
        self.assertEqual(treasure.description, "New description")
        self.assertEqual(treasure.creator, self.user)
        self.assertEqual(treasure.creator.handle, self.user.handle)

    def test_update_method(self):
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
            "description": "Updated description.",
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
        updated = serializer.save()

        # Refresh from database to ensure we're seeing saved changes
        updated.refresh_from_db()

        # Check writable fields - SHOULD be updated
        self.assertEqual(updated.name, "Updated Name")
        self.assertEqual(updated.category, "Updated Category")
        self.assertEqual(
            updated.description,
            "Updated description.",
        )

        # Check read-only fields - should NOT be updated
        self.assertEqual(updated.id, self.treasure_data["id"])
        self.assertEqual(updated.creator, self.user)
        self.assertEqual(updated.date_added, self.treasure_data["date_added"])

        # last_modified is a special case - it should be updated automatically because of auto_now=True
        # but not to our specified value
        self.assertNotEqual(
            updated.last_modified, self.treasure_data["last_modified"]
        )  # Should be changed
        self.assertNotEqual(
            updated.last_modified.isoformat(), "2020-01-01T00:00:00+00:00"
        )  # But not to our value

        # Check computed properties - should reflect the new values of the underlying fields
        expected_new_short_details = (
            f"Updated Name - Updated Category by {self.user.handle}"
        )
        self.assertEqual(updated.short_details, expected_new_short_details)

        # For truncated_description
        self.assertIn(update_data["name"], updated.truncated)
        self.assertIn(self.user.handle, updated.truncated)
        self.assertIn(update_data["description"][:50], updated.truncated)
        if len(update_data["description"]) > 50:
            self.assertIn("...", updated_treasure.truncated)

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

    def test_optional_fields(self):
        """Test that optional fields can be omitted"""
        # Assuming category is optional
        data = {"name": "No Category", "description": "This treasure has no category"}
        serializer = TreasureSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        treasure = serializer.save(creator=self.user)
        self.assertEqual(treasure.category, "")  # Or None, depending on your model

    def test_validate_name_not_blank(self):
        """Test that name validation rejects blank names"""
        # Test with blank name
        data = {"name": "   "}  # Just spaces
        serializer = TreasureSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        e = context.exception
        self.assertIn("name", str(e))
        self.assertIn("blank", str(e))

    def test_unknown_field_rejection(self):
        """Test that unknown fields are rejected based on BaseSerializerMixin"""
        data = {"name": "Valid Name", "unknown_field": "This should cause an error"}

        serializer = TreasureSerializer(data=data)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        e = context.exception
        self.assertIn("unknown_field", str(e))
        self.assertIn("invalid", str(e))

    def test_deserialization_from_json(self):
        """Test that serializer can deserialize JSON data correctly"""
        json_data = {
            "name": "JSON Treasure",
            "category": "Deserialized",
            "description": "This treasure was created from JSON data",
        }
        serializer = TreasureSerializer(data=json_data)
        self.assertTrue(serializer.is_valid())
        treasure = serializer.save(creator=self.user)
        self.assertEqual(treasure.name, "JSON Treasure")
        self.assertEqual(treasure.category, "Deserialized")
        self.assertEqual(
            treasure.description, "This treasure was created from JSON data"
        )
        self.assertEqual(treasure.creator, self.user)

    def test_name_max_length(self):
        """Test that name field enforces max length"""
        # Assuming name has a max length (check your model definition)
        max_length = 100  # Adjust based on your model's actual max_length
        data = {
            "name": "X" * (max_length + 1),
            "category": "Test",
            "description": "Description",
        }
        serializer = TreasureSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("max_length", str(serializer.errors["name"]))

    def test_empty_description(self):
        """Test that description can be empty if allowed by the model"""
        data = {
            "name": "Empty Description",
            "category": "Test Category",
            "description": "",
        }
        serializer = TreasureSerializer(data=data)
        # This assertion depends on whether your model allows empty descriptions
        serializer.is_valid()
        self.assertIn("description", serializer.errors)
        self.assertIn("blank", str(serializer.errors["description"]))
