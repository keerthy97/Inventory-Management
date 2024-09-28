from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from inventory.models import Item
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class ItemViewSetTests(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a token for the user if using token authentication
        self.token = Token.objects.create(user=self.user)

        # Force authenticate the client with the user
        self.client.force_authenticate(user=self.user)

        # Create an Item instance for testing
        self.item = Item.objects.create(name='Laptop', description='A powerful laptop', quantity=10, price='1500.00')

    def test_retrieve_item(self):
        """Test retrieving an existing item."""
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_retrieve_non_existent_item(self):
        """Test retrieving a non-existent item."""
        url = reverse('item-detail', args=[999])  # Assuming 999 doesn't exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item(self):
        """Test updating an existing item."""
        url = reverse('item-detail', args=[self.item.id])
        data = {'name': 'Updated Laptop', 'quantity': 15}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Laptop')
        self.assertEqual(self.item.quantity, 15)

    def test_update_non_existent_item(self):
        """Test updating a non-existent item."""
        url = reverse('item-detail', args=[999])  # Assuming 999 doesn't exist
        data = {'name': 'Non-existent Item'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_item(self):
        """Test deleting an existing item."""
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

    def test_destroy_non_existent_item(self):
        """Test deleting a non-existent item."""
        url = reverse('item-detail', args=[999])  # Assuming 999 doesn't exist
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

