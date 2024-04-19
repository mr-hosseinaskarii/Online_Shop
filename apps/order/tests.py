from django.test import TestCase
from django.utils import timezone
from .models import OrderItem, Order, STATUS_CHOICE
from apps.shop.models import Product
from apps.account.models import CustomUser


class OrderItemModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', description='Test Description', price=100, amount=10)
        self.order_item_data = {
            'product': self.product,
            'quantity': 2,
            'price': 200
        }

    def test_order_item_creation(self):
        # Test creating an order item
        order_item = OrderItem.objects.create(**self.order_item_data)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, 200)


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='test@example.com', phone_number='+989123456789', password='Test@1234')
        self.order_data = {
            'user': self.user,
            'total_amount': 300,
            'status': 'Pending'
        }

    def test_order_creation(self):
        # Test creating an order
        order = Order.objects.create(**self.order_data)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_amount, 300)
        self.assertEqual(order.status, 'Pending')

    def test_order_date_auto_now_add(self):
        # Test that order_date is automatically set to current time on creation
        order = Order.objects.create(**self.order_data)
        self.assertIsNotNone(order.order_date)
        self.assertTrue(timezone.now() - order.order_date < timezone.timedelta(seconds=1))

    def test_order_status_choices(self):
        # Test that status choices are respected
        for choice in STATUS_CHOICE:
            self.order_data['status'] = choice[0]
            order = Order.objects.create(**self.order_data)
            self.assertEqual(order.status, choice[0])

    def test_order_total_amount_negative(self):
        # Test that total_amount cannot be negative
        self.order_data['total_amount'] = -100
        with self.assertRaises(ValueError):
            Order.objects.create(**self.order_data)

    def test_order_related_name(self):
        # Test related_name 'orders' for CustomUser
        self.assertEqual(list(self.user.orders.all()), [])
        order = Order.objects.create(**self.order_data)
        self.assertEqual(list(self.user.orders.all()), [order])

    def test_order_related_name_for_order_items(self):
        # Test related_name 'order_items' for Order
        order = Order.objects.create(**self.order_data)
        self.assertEqual(list(order.order_items.all()), [])

        # Assuming there's an OrderItem model related to Order, create an OrderItem associated with this order
        # Replace OrderItem.objects.create with your actual creation logic
        # order_item = OrderItem.objects.create(order=order, ...)
        # self.assertEqual(list(order.order_items.all()), [order_item])
