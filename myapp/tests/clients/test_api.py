from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from clients.models import Order, OrderPosition

User = get_user_model()

class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_supplier_orders_view(self):
        response = self.client.get('/supplier/orders/')
        self.assertEqual(response.status_code, 200)

    def test_cart_view_get(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_cart_view_post(self):
        response = self.client.post('/cart/', {'goods': [{'product': 1, 'quantity': 2}]}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_cart_view_delete(self):
        response = self.client.delete('/cart/', {'goods': '1,2,3'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_client_view_get(self):
        response = self.client.get('/client/')
        self.assertEqual(response.status_code, 200)

    def test_client_view_post(self):
        response = self.client.post('/client/', {'goods': [{'product': 1, 'quantity': 2}]}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_order_creation(self):
            order = Order.objects.create(user_id=1, state='new')
            self.assertEqual(order.state, 'new')

    def test_order_position_creation(self):
            order = Order.objects.create(user_id=1, state='new')
            order_position = OrderPosition.objects.create(order=order, product_id=1, quantity=2)
            self.assertEqual(order_position.quantity, 2)