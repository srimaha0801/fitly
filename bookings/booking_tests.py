from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ClassList, Client
from datetime import datetime

class SimpleBookingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fitness_class = ClassList.objects.create(
            class_name="Zumba",
            instructor="John",
            total_slots=10,
            available_slots=10,
            date=datetime(2025, 6, 9, 18, 0)
        )
        self.url = '/book/'
        self.payload = {
            "class_id": self.fitness_class.id,
            "client_name": "Alice",
            "client_email": "alice@example.com"
        }

    def test_successful_booking(self):
        response = self.client.post(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.first().enrolled_classes.count(), 1)
        self.assertEqual(ClassList.objects.first().available_slots, 9)
