from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item
import os
import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventory_management.settings")
django.setup()

class ItemTests(APITestCase):
    def test_create_item(self):
        url = reverse('item-list')
        data = {'name': 'Laptop', 'description': 'A gaming laptop', 'quantity': 10, 'price': '1200.00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_item(self):
        item = Item.objects.create(name='Phone', description='A smartphone', quantity=20, price='500.00')
        url = reverse('item-detail', kwargs={'pk': item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
