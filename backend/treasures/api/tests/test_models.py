from django.test import TestCase
from django.contrib.auth import get_user_model
from treasures.models import Treasure
from django.utils import timezone
from datetime import timedelta, datetime

User = get_user_model()


class TreasureModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email="testuser@example.com", handle="testuser", password="password123"
        )

        # Create a test treasure
        self.treasure = Treasure.objects.create(
            name="name",
            category="category",
            creator=self.user,
            description="description",
        )

    def test_treasure_creation(self):
        """Test that a treasure can be created with all fields"""
        # Get initial count
        initial_count = Treasure.objects.count()

        # Create treasure in the test method, not setUp
        treasure = Treasure.objects.create(
            name="Declaration of Independence",
            category="Historical Document",
            creator=self.user,
            description="It has a map on the back that leads to treasure.",
        )
        creation_time = timezone.now()
        # Verify object exists in database
        self.assertTrue(Treasure.objects.filter(id=treasure.id).exists())

        # Verify count increased
        self.assertEqual(Treasure.objects.count(), initial_count + 1)

        # Verify field values were stored correctly
        self.assertEqual(treasure.name, "Declaration of Independence")
        self.assertEqual(treasure.category, "Historical Document")
        self.assertEqual(treasure.creator, self.user)
        self.assertEqual(
            treasure.description, "It has a map on the back that leads to treasure."
        )
        self.assertIn(treasure, self.user.treasure_set.all())
        self.assertEqual(
            treasure.date_added.replace(microsecond=0),
            creation_time.replace(microsecond=0),
        )
        self.assertEqual(
            treasure.last_modified.replace(microsecond=0),
            creation_time.replace(microsecond=0),
        )

    def test_treasure_read(self):
        """Test that a treasure can be created with all fields"""
        self.assertEqual(self.treasure.name, "name")
        self.assertEqual(self.treasure.category, "category")
        self.assertEqual(self.treasure.creator, self.user)
        self.assertEqual(self.treasure.description, "description")
        self.assertIn(self.treasure, self.user.treasure_set.all())

        # Test auto fields
        self.assertIsNotNone(self.treasure.date_added)
        self.assertIsNotNone(self.treasure.last_modified)

    def test_string_representation(self):
        """Test the string representation of a Treasure"""
        expected_str = "testuser feels that name is a National Treasure. Their reasoning is that description."
        self.assertEqual(str(self.treasure), expected_str)

    def test_ignore_fields_property(self):
        """Test the ignore_fields property returns the correct fields"""
        ignore_fields = self.treasure.ignore_fields
        self.assertIsInstance(ignore_fields, set)
        self.assertEqual(
            ignore_fields, {"id", "creator", "date_added", "last_modified"}
        )

    def test_short_details_property(self):
        """Test the short_details property returns the correct format"""
        expected = "name - category by testuser"
        self.assertEqual(self.treasure.short_details, expected)

    def test_without_truncation(self):
        """Test the abbrev property for short descriptions"""
        sdt = Treasure.objects.create(
            name="Liberty Bell",
            category="Monument",
            creator=self.user,
            description="It's cracked but still beautiful.",
        )

        expected = "Liberty Bell - testuser for It's cracked but still beautiful."
        self.assertEqual(sdt.truncated, expected)

    def test_with_truncation(self):
        """Test the abbrev property truncates long descriptions"""
        long_desc = "This is a very long description that exceeds fifty characters and should be truncated by the abbrev property to ensure readability while still providing context about the treasure that is being described."
        long_desc_treasure = Treasure.objects.create(
            name="Statue of Liberty",
            category="Monument",
            creator=self.user,
            description=long_desc,
        )

        expected = f"Statue of Liberty - testuser for {long_desc[:50]}..."
        self.assertEqual(long_desc_treasure.truncated, expected)

    def test_auto_now_fields(self):
        """Test that date_added doesn't change but last_modified does on update"""
        original_date_added = self.treasure.date_added
        original_last_modified = self.treasure.last_modified

        # Wait a moment to ensure time difference
        import time

        time.sleep(0.1)

        # Update the treasure
        self.treasure.name = "Updated Name"
        self.treasure.save()

        # Refresh from database
        self.treasure.refresh_from_db()

        # date_added should not change
        self.assertEqual(self.treasure.date_added, original_date_added)

        # last_modified should change
        self.assertGreater(self.treasure.last_modified, original_last_modified)

    def test_cascade_deletion(self):
        """Test that treasures are deleted when the creator is deleted"""
        treasure_id = self.treasure.id

        # Delete the user
        self.user.delete()

        # Check that the treasure was also deleted (CASCADE)
        self.assertFalse(Treasure.objects.filter(id=treasure_id).exists())

    def test_update_treasure_with_valid_data(self):
        """Test updating a treasure with valid data"""
        # Initial state
        self.assertEqual(self.treasure.name, "name")
        self.assertEqual(self.treasure.category, "category")

        # Update the treasure
        self.treasure.name = "Updated Treasure"
        self.treasure.category = "Updated Category"
        self.treasure.description = "Updated description"
        self.treasure.save()

        # Refresh from database
        self.treasure.refresh_from_db()

        # Check updated values
        self.assertEqual(self.treasure.name, "Updated Treasure")
        self.assertEqual(self.treasure.category, "Updated Category")
        self.assertEqual(self.treasure.description, "Updated description")

    def test_update_treasure_with_invalid_data(self):
        """Test updating a treasure with invalid data (name too long)"""
        # Try to set name that exceeds max_length
        self.treasure.name = "x" * 101  # Exceeds the 100 char limit

        # This should raise a validation error
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            self.treasure.full_clean()  # This validates the model

    def test_delete_treasure(self):
        """Test deleting a treasure"""
        # Get initial count
        initial_count = Treasure.objects.count()
        treasure_id = self.treasure.id

        # Delete the treasure
        self.treasure.delete()

        # Check it's gone from the database
        self.assertEqual(Treasure.objects.count(), initial_count - 1)
        self.assertFalse(Treasure.objects.filter(id=treasure_id).exists())

    def test_name_cannot_be_blank(self):
        """Test that a treasure's name cannot be blank"""
        # Try creating with blank name
        from django.core.exceptions import ValidationError

        treasure = Treasure(
            name="",  # Blank name
            category="Test Category",
            creator=self.user,
            description="Test description",
        )

        # This should raise a validation error
        with self.assertRaises(ValidationError):
            treasure.full_clean()

        # Alternatively, test in-place update with blank name
        self.treasure.name = ""
        with self.assertRaises(ValidationError):
            self.treasure.full_clean()

    def test_treasure_with_empty_description(self):
        """Test that a treasure can be created with an empty description"""
        treasure = Treasure.objects.create(
            name="Empty Description Treasure",
            category="Test Category",
            creator=self.user,
            description="",
        )
        treasure.refresh_from_db()
        self.assertEqual(treasure.description, "")
        # Check string representation with empty description
        expected_str = f"{self.user.handle} feels that Empty Description Treasure is a National Treasure. Their reasoning is that ."
        self.assertEqual(str(treasure), expected_str)

    def test_treasure_with_special_characters(self):
        """Test that a treasure can handle special characters in fields"""
        special_name = "Spécïål Trëasüre ☺ 测试"
        special_category = "émojí & unicode ✓ 分类"
        special_description = (
            "This description has §pécial ©hara¢ters and emoji 🏆 🌟 ✨"
        )

        treasure = Treasure.objects.create(
            name=special_name,
            category=special_category,
            creator=self.user,
            description=special_description,
        )
        treasure.refresh_from_db()

        self.assertEqual(treasure.name, special_name)
        self.assertEqual(treasure.category, special_category)
        self.assertEqual(treasure.description, special_description)

        # Test properties with special characters
        expected_short = f"{special_name} - {special_category} by {self.user.handle}"
        self.assertEqual(treasure.short_details, expected_short)

    def test_short_details_with_empty_category(self):
        """Test the short_details property with an empty category"""
        treasure = Treasure.objects.create(
            name="No Category Treasure",
            category="",
            creator=self.user,
            description="A treasure with no category",
        )

        expected = "No Category Treasure -  by testuser"
        self.assertEqual(treasure.short_details, expected)

    def test_with_exactly_50_char_description(self):
        """Test the abbrev property with exactly 50 characters (boundary case)"""
        exactly_50_chars = "This description is exactly fifty characters long."
        self.assertEqual(len(exactly_50_chars), 50)

        treasure = Treasure.objects.create(
            name="Boundary Case",
            category="Test",
            creator=self.user,
            description=exactly_50_chars,
        )

        # No ellipsis should be added since it's exactly 50 chars
        expected = f"Boundary Case - testuser for {exactly_50_chars}"
        self.assertEqual(treasure.truncated, expected)

    def test_user_with_multiple_treasures(self):
        """Test a user with multiple treasures"""
        # Already have one treasure from setUp
        initial_count = self.user.treasure_set.count()

        # Add two more treasures
        treasure2 = Treasure.objects.create(
            name="Second Treasure",
            category="Category2",
            creator=self.user,
            description="Second treasure description",
        )

        treasure3 = Treasure.objects.create(
            name="Third Treasure",
            category="Category3",
            creator=self.user,
            description="Third treasure description",
        )

        # Test that user has all treasures
        self.assertEqual(self.user.treasure_set.count(), initial_count + 2)
        user_treasures = self.user.treasure_set.all()
        self.assertIn(self.treasure, user_treasures)
        self.assertIn(treasure2, user_treasures)
        self.assertIn(treasure3, user_treasures)

    def test_treasure_with_minimum_required_fields(self):
        """Test creating a treasure with only the required fields"""
        # According to the model, only name is required (has blank=False)
        treasure = Treasure.objects.create(
            name="Minimal Treasure",
            creator=self.user,
        )

        treasure.refresh_from_db()
        self.assertEqual(treasure.name, "Minimal Treasure")
        self.assertEqual(treasure.category, "")  # Default for CharField
        self.assertEqual(treasure.description, "")  # Default for TextField
        self.assertIsNotNone(treasure.date_added)
        self.assertIsNotNone(treasure.last_modified)
