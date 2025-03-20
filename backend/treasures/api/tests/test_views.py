from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from unittest import skip
import json

from treasures.models import Treasure
from treasures.api.serializers import TreasureSerializer


User = get_user_model()


class TreasureViewSetTestBase(APITestCase):
    """Base test case for TreasureViewSet tests with users and treasures setup"""

    def setUp(self):
        # Create a normal user
        self.user = User.objects.create_user(
            email="user@example.com", handle="normaluser", password="password123"
        )

        # Create a superuser
        self.superuser = User.objects.create_superuser(
            email="admin@example.com", handle="adminuser", password="adminpass123"
        )

        # Create treasures for normal user
        self.user_treasures = []
        for i in range(3):
            treasure = Treasure.objects.create(
                creator=self.user,
                name=f"User Treasure {i+1}",
                category=f"Category {i+1}",
                description=f"Description for user treasure {i+1}",
            )
            self.user_treasures.append(treasure)

        # Create treasures for superuser
        self.superuser_treasures = []
        for i in range(3):
            treasure = Treasure.objects.create(
                creator=self.superuser,
                name=f"Admin Treasure {i+1}",
                category=f"Admin Category {i+1}",
                description=f"Description for admin treasure {i+1}",
            )
            self.superuser_treasures.append(treasure)

        # Set up API client
        self.client = APIClient()

        # URLs
        self.list_url = reverse(
            "treasure-list"
        )  # Assuming 'treasure-list' is the name of the list route

    def get_detail_url(self, treasure_id):
        """Helper method to get detail URL for a specific treasure"""
        return reverse(
            "treasure-detail", args=[treasure_id]
        )  # Assuming 'treasure-detail' is the name

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def authenticate(self, user):
        token = self.get_tokens_for_user(user)["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")


class TreasureViewSetUnitTests(TreasureViewSetTestBase):
    """Unit tests for TreasureViewSet"""

    def test_list_treasures_authenticated(self):
        """Test that authenticated users can list their own treasures"""
        # Login as normal user
        self.authenticate(self.user)

        # Get list of treasures
        response = self.client.get(self.list_url)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that only user's treasures are returned
        self.assertEqual(
            len(response.data["results"]), 3
        )  # Assuming pagination is enabled

        # Verify the returned treasures belong to the user
        treasure_ids = [item["id"] for item in response.data["results"]]
        user_treasure_ids = [treasure.id for treasure in self.user_treasures]
        self.assertEqual(set(treasure_ids), set(user_treasure_ids))

    def test_list_treasures_unauthenticated(self):
        """Test that unauthenticated users cannot list treasures"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_own_treasure(self):
        """Test that users can retrieve their own treasures"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Get a specific treasure
        treasure = self.user_treasures[0]
        url = self.get_detail_url(treasure.id)
        response = self.client.get(url)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], treasure.id)
        self.assertEqual(response.data["name"], treasure.name)
        self.assertEqual(response.data["creator"], self.user.id)

    def test_retrieve_other_user_treasure(self):
        """Test that users cannot retrieve other users' treasures"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Try to get a superuser's treasure
        treasure = self.superuser_treasures[0]
        url = self.get_detail_url(treasure.id)
        response = self.client.get(url)

        # Should return 404 as the queryset is filtered to user's treasures
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_treasure(self):
        """Test creating a new treasure"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Data for new treasure
        data = {
            "name": "New Test Treasure",
            "category": "Test Category",
            "description": "This is a test treasure created via API",
        }

        # Create treasure
        response = self.client.post(self.list_url, data, format="json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["category"], data["category"])
        self.assertEqual(response.data["description"], data["description"])
        self.assertEqual(response.data["creator"], self.user.id)

        # Verify treasure was created in database
        treasure_id = response.data["id"]
        treasure = Treasure.objects.get(id=treasure_id)
        self.assertEqual(treasure.name, data["name"])
        self.assertEqual(treasure.creator, self.user)

    def test_update_own_treasure(self):
        """Test updating own treasure"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Get a treasure to update
        treasure = self.user_treasures[0]
        url = self.get_detail_url(treasure.id)

        # Update data
        data = {
            "name": "Updated Treasure Name",
            "category": "Updated Category",
            "description": "Updated description",
        }

        # Update treasure
        response = self.client.put(url, data, format="json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["category"], data["category"])
        self.assertEqual(response.data["description"], data["description"])

        # Verify treasure was updated in database
        treasure.refresh_from_db()
        self.assertEqual(treasure.name, data["name"])
        self.assertEqual(treasure.category, data["category"])
        self.assertEqual(treasure.description, data["description"])

    def test_partial_update_own_treasure(self):
        """Test partially updating own treasure"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Get a treasure to update
        treasure = self.user_treasures[0]
        url = self.get_detail_url(treasure.id)

        # Partial update data
        data = {"name": "Partially Updated Name"}

        # Update treasure
        response = self.client.patch(url, data, format="json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

        # Original category and description should be unchanged
        self.assertEqual(response.data["category"], treasure.category)
        self.assertEqual(response.data["description"], treasure.description)

        # Verify treasure was updated in database
        treasure.refresh_from_db()
        self.assertEqual(treasure.name, data["name"])

    def test_delete_own_treasure(self):
        """Test deleting own treasure"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Get a treasure to delete
        treasure = self.user_treasures[0]
        url = self.get_detail_url(treasure.id)

        # Delete treasure
        response = self.client.delete(url)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify treasure was deleted from database
        with self.assertRaises(Treasure.DoesNotExist):
            Treasure.objects.get(id=treasure.id)

    def test_update_other_user_treasure(self):
        """Test that users cannot update other users' treasures"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Try to update a superuser's treasure
        treasure = self.superuser_treasures[0]
        url = self.get_detail_url(treasure.id)

        data = {"name": "Attempt to Update Other User's Treasure"}

        # Try to update
        response = self.client.patch(url, data, format="json")

        # Should return 404 as the queryset is filtered to user's treasures
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify treasure was not updated
        treasure.refresh_from_db()
        self.assertNotEqual(treasure.name, data["name"])

    def test_delete_other_user_treasure(self):
        """Test that users cannot delete other users' treasures"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Try to delete a superuser's treasure
        treasure = self.superuser_treasures[0]
        url = self.get_detail_url(treasure.id)

        # Try to delete
        response = self.client.delete(url)

        # Should return 404 as the queryset is filtered to user's treasures
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify treasure was not deleted
        self.assertTrue(Treasure.objects.filter(id=treasure.id).exists())


class TreasureViewSetIntegrationTests(TreasureViewSetTestBase):
    """Integration tests for TreasureViewSet"""

    def test_create_and_retrieve_flow(self):
        """Test the full flow of creating and then retrieving a treasure"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Create a new treasure
        create_data = {
            "name": "Integration Test Treasure",
            "category": "Integration",
            "description": "This treasure tests the full create-retrieve flow",
        }

        create_response = self.client.post(self.list_url, create_data, format="json")
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Get the ID of the created treasure
        treasure_id = create_response.data["id"]

        # Retrieve the treasure
        detail_url = self.get_detail_url(treasure_id)
        retrieve_response = self.client.get(detail_url)

        # Check that retrieved data matches what we created
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data["id"], treasure_id)
        self.assertEqual(retrieve_response.data["name"], create_data["name"])
        self.assertEqual(retrieve_response.data["category"], create_data["category"])
        self.assertEqual(
            retrieve_response.data["description"], create_data["description"]
        )
        self.assertEqual(retrieve_response.data["creator"], self.user.id)
        self.assertEqual(retrieve_response.data["creator_handle"], self.user.handle)

    def test_create_update_delete_flow(self):
        """Test the full flow of creating, updating, and then deleting a treasure"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Create a new treasure
        create_data = {
            "name": "CRUD Flow Treasure",
            "category": "CRUD Test",
            "description": "This treasure tests the full CRUD flow",
        }

        create_response = self.client.post(self.list_url, create_data, format="json")
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Get the ID of the created treasure
        treasure_id = create_response.data["id"]
        detail_url = self.get_detail_url(treasure_id)

        # Update the treasure
        update_data = {
            "name": "Updated CRUD Flow Treasure",
            "description": "This description has been updated",
        }

        update_response = self.client.patch(detail_url, update_data, format="json")
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["name"], update_data["name"])
        self.assertEqual(
            update_response.data["description"], update_data["description"]
        )
        self.assertEqual(
            update_response.data["category"], create_data["category"]
        )  # Unchanged

        # Delete the treasure
        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it's gone
        get_response = self.client.get(detail_url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pagination(self):
        """Test that pagination works correctly"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Create more treasures to test pagination (assuming page_size=10)
        for i in range(15):
            Treasure.objects.create(
                creator=self.user,
                name=f"Pagination Test Treasure {i+1}",
                category="Pagination",
                description=f"Description for pagination test treasure {i+1}",
            )

        # Get first page
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("count", response.data)

        # We should have 10 results per page (default page_size)
        self.assertEqual(len(response.data["results"]), 10)

        # Total count should be 18 (3 original + 15 new)
        self.assertEqual(response.data["count"], 18)

        # Get second page
        if response.data["next"]:
            response = self.client.get(response.data["next"])
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data["results"]), 8)  # Remaining 8 items

    def test_custom_page_size(self):
        """Test that custom page_size query parameter works"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Create more treasures
        for i in range(10):
            Treasure.objects.create(
                creator=self.user,
                name=f"Custom Page Size Test {i+1}",
                category="Pagination",
                description=f"Description for custom page size test {i+1}",
            )

        # Request with custom page size
        response = self.client.get(f"{self.list_url}?page_size=5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

        # Total count should be 13 (3 original + 10 new)
        self.assertEqual(response.data["count"], 13)


@skip
class CopyTreasureViewTest(TreasureViewSetTestBase):
    """Tests for the copy_treasure view function"""

    def setUp(self):
        super().setUp()
        # URL for copy_treasure view
        self.copy_url = reverse("copy-treasure", args=[self.superuser_treasures[0].id])

    def test_copy_treasure_authenticated(self):
        """Test that authenticated users can copy treasures"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Copy a treasure
        response = self.client.post(self.copy_url)

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode(), "Treasure copied")

        # Verify a new treasure was created
        original_treasure = self.superuser_treasures[0]
        copied_treasures = Treasure.objects.filter(
            name=original_treasure.name,
            category=original_treasure.category,
            description=original_treasure.description,
            creator=self.user,
        )

        self.assertEqual(copied_treasures.count(), 1)
        copied_treasure = copied_treasures.first()

        # Verify the copied treasure has the correct attributes
        self.assertEqual(copied_treasure.name, original_treasure.name)
        self.assertEqual(copied_treasure.category, original_treasure.category)
        self.assertEqual(copied_treasure.description, original_treasure.description)
        self.assertEqual(copied_treasure.creator, self.user)

        # Verify it's a different object
        self.assertNotEqual(copied_treasure.id, original_treasure.id)

    def test_copy_nonexistent_treasure(self):
        """Test copying a nonexistent treasure"""
        # Login as normal user
        self.client.force_authenticate(user=self.user)

        # Try to copy a nonexistent treasure
        url = reverse("copy-treasure", args=[99999])  # Assuming this ID doesn't exist
        response = self.client.post(url)

        # Should return 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_copy_treasure_unauthenticated(self):
        """Test that unauthenticated users cannot copy treasures"""
        response = self.client.post(self.copy_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
