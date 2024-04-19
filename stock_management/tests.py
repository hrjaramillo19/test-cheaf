from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TokenAPITestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="test_user", email="test_user@email.com", password="test_password"
        )
        cls.client = APIClient()

    def test_valid_token(self):
        data = {"username": "test_user", "password": "test_password"}
        response = self.client.post("/api/v1/token/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_token(self):
        data = {"username": "test_user", "password": "test"}
        response = self.client.post("/api/v1/token/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
