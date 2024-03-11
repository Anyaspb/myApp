import json
from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from suppliers.models import Product, Category, Supplier

#
# @pytest.fixture
# def user():
#     # Create a user
#     user = User.objects.create_user(username='test_user', password='test_password')
#     return user
#
# @pytest.fixture
# def authenticated_client(user):
#     # Create a Django test client
#     client = Client()
#     # Log in the user
#     client.force_login(user)
#     return client

class TestViews(TestCase):

    def test_catalog_view(self):
        response = self.client.get('/catalog/products/')
        self.assertEqual(response.status_code, 200)

    def test_price_update_view(self):
        data = {'markup': 10}
        response = self.client.post('/catalog/price-update/', data=data)
        assert response.status_code == 200

    def test_product_view(self):
        response = self.client.get('/catalog/products/')
        self.assertEqual(response.status_code, 200)

    def test_category_view(self):
        response = self.client.get('/catalog/category/')
        self.assertEqual(response.status_code, 200)

    def test_supplier_view(self):
        response = self.client.get('/catalog/supplier/')
        self.assertEqual(response.status_code, 200)

    def test_supplier_state_view(self):
        response = self.client.get('/catalog/supplier-state/')
        self.assertEqual(response.status_code, 200)


