import logging

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from .models import CustomUser, Address

# Set up logging
logger = logging.getLogger(__name__)


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'phone_number': '+989123456789',
            'password': 'Test@1234',
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'male',
            'is_verified': True,
            'is_admin': True,
            'is_staff': True,
            'is_active': True,
            'is_superuser': True
        }

    def test_create_user(self):
        # Test creating a user
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        logger.info(f"User {user.email} created successfully.")

    def test_email_validation(self):
        # Test email validation
        invalid_email_data = {
            'email': 'invalidemail.com',
            'phone_number': '+989123456789',
            'password': 'Test@1234'
        }
        with self.assertRaises(ValidationError):
            CustomUser.objects.create(**invalid_email_data)
        logger.info("Invalid email data validation passed.")

    def test_phone_number_validation(self):
        # Test phone number validation
        invalid_phone_data = {
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password': 'Test@1234'
        }
        with self.assertRaises(ValidationError):
            CustomUser.objects.create(**invalid_phone_data)
        logger.info("Invalid phone number data validation passed.")

    def test_password_validation(self):
        # Test password validation
        invalid_password_data = {
            'email': 'test@example.com',
            'phone_number': '+989123456789',
            'password': 'password123'
        }
        with self.assertRaises(ValidationError):
            CustomUser.objects.create(**invalid_password_data)
        logger.info("Invalid password data validation passed.")

    def test_user_str_representation(self):
        # Test __str__ method of CustomUser model
        user = CustomUser.objects.create(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])
        logger.info("User string representation test passed.")

    def test_user_permissions(self):
        # Test user permissions
        user = CustomUser.objects.create(**self.user_data)
        self.assertTrue(user.has_perm('test_permission'))
        self.assertTrue(user.has_module_perms('test_module'))
        logger.info("User permissions test passed.")

    def test_user_registration_time(self):
        # Test user registration time
        user = CustomUser.objects.create(**self.user_data)
        self.assertIsNotNone(user.registered_on)
        logger.info("User registration time test passed.")

    def test_user_last_login_time(self):
        # Test user last login time
        user = CustomUser.objects.create(**self.user_data)
        user.last_login = timezone.now()
        user.save()
        self.assertIsNotNone(user.last_login)
        logger.info("User last login time test passed.")


class AddressModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='test@example.com', phone_number='+989123456789', password='Test@1234')
        self.address_data = {
            'user': self.user,
            'country': 'USA',
            'state': 'California',
            'city': 'Los Angeles',
            'street': '123 Main St',
            'no': 101,
            'postal_code': '90001'
        }

    def test_address_creation(self):
        # Test creating an address
        address = Address.objects.create(**self.address_data)
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.country, 'USA')
        self.assertEqual(address.state, 'California')
        self.assertEqual(address.city, 'Los Angeles')
        self.assertEqual(address.street, '123 Main St')
        self.assertEqual(address.no, 101)
        self.assertEqual(address.postal_code, '90001')

    def test_address_user_relationship(self):
        # Test user-address relationship and related_name
        self.assertEqual(list(self.user.addresses.all()), [])
        address = Address.objects.create(**self.address_data)
        self.assertEqual(list(self.user.addresses.all()), [address])

    def test_address_no_negative(self):
        # Test that 'no' field cannot be negative
        self.address_data['no'] = -101
        with self.assertRaises(ValueError):
            Address.objects.create(**self.address_data)

    def test_address_postal_code_length(self):
        # Test maximum length validation for 'postal_code'
        self.address_data['postal_code'] = '1234567890'  # Length greater than 10
        with self.assertRaises(ValueError):
            Address.objects.create(**self.address_data)

    def test_address_str_representation(self):
        # Test __str__ method of Address model
        address = Address.objects.create(**self.address_data)
        expected_str = f"{address.no} {address.street}, {address.city}, {address.state}, {address.country} - {address.postal_code}"
        self.assertEqual(str(address), expected_str)

    def test_address_unique_together(self):
        # Test that no combination of user, street, and postal_code can be duplicated
        Address.objects.create(**self.address_data)
        with self.assertRaises(Exception):
            Address.objects.create(**self.address_data)
