from django.test import TestCase
from .models import Product, Category


class CategoryModelTestCase(TestCase):
    def setUp(self):
        # Create some categories for testing
        self.parent_category = Category.objects.create(name='Parent Category')
        self.child_category = Category.objects.create(name='Child Category', parent=self.parent_category)

    def test_category_creation(self):
        # Test category creation
        parent_category = Category.objects.get(name='Parent Category')
        child_category = Category.objects.get(name='Child Category')

        self.assertEqual(parent_category.name, 'Parent Category')
        self.assertIsNone(parent_category.parent)  # Parent category should not have a parent
        self.assertEqual(child_category.name, 'Child Category')
        self.assertEqual(child_category.parent, self.parent_category)  # Child category should have the parent set correctly

    def test_category_str_representation(self):
        # Test __str__ method of Category model
        parent_category = Category.objects.get(name='Parent Category')
        child_category = Category.objects.get(name='Child Category')

        self.assertEqual(str(parent_category), 'Parent Category')
        self.assertEqual(str(child_category), 'Child Category')

    def test_category_children_relationship(self):
        # Test related_name 'children' for parent category
        self.assertEqual(list(self.parent_category.children.all()), [self.child_category])  # Parent category should have the child category

    def test_orphan_category_creation(self):
        # Test category creation without a parent
        orphan_category = Category.objects.get(name='Orphan Category')

        self.assertEqual(orphan_category.name, 'Orphan Category')
        self.assertIsNone(orphan_category.parent)  # Orphan category should not have a parent

    def test_parent_category_has_no_children(self):
        # Test if a category without children returns an empty list
        parent_category_no_children = Category.objects.create(name='No Children Category')

        self.assertEqual(list(parent_category_no_children.children.all()), [])  # The list of children should be empty

    def test_category_update(self):
        # Test updating the name of a category
        self.parent_category.name = 'Updated Parent Category'
        self.parent_category.save()

        updated_parent_category = Category.objects.get(id=self.parent_category.id)
        self.assertEqual(updated_parent_category.name, 'Updated Parent Category')


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            description='Test Description',
            price=100,
            amount=10,
            discount=20,
            max_discount_amount=50,
            min_discount_amount=0
        )

    def test_discounted_price_calculation(self):
        # Test that discounted price is calculated correctly
        self.assertEqual(self.product.discounted_price, 80)  # 100 - 50 (max_discount_amount) = 50, 20% discount on 50 = 10, 100 - 10 = 90

    def test_discounted_price_with_full_discount(self):
        # Test when the discount is set to 100%
        self.product.discount = 100
        self.assertEqual(self.product.discounted_price, 50)  # 100 - 50 (max_discount_amount) = 50, 100% discount on 50 = 50, 100 - 50 = 50

    def test_discounted_price_with_no_discount(self):
        # Test when there's no discount
        self.product.discount = 0
        self.assertEqual(self.product.discounted_price, 100)  # No discount applied, so the price should remain 100

    def test_discounted_price_with_zero_max_discount_amount(self):
        # Test when max_discount_amount is set to zero
        self.product.max_discount_amount = 0
        self.assertEqual(self.product.discounted_price, 80)  # No maximum discount amount applied, so the discounted price should be the same as the regular price

    def test_discounted_price_with_large_discount(self):
        # Test when the discount amount exceeds the maximum discount amount
        self.product.discount = 50
        self.assertEqual(self.product.discounted_price, 75)  # 100 - 50 (max_discount_amount) = 50, 50% discount on 50 = 25, 100 - 25 = 75

    def test_discounted_price_with_negative_discount(self):
        # Test when a negative discount is applied
        self.product.discount = -10
        self.assertEqual(self.product.discounted_price, 110)  # Negative discount should increase the price

    def test_discounted_price_with_max_discount_amount_greater_than_price(self):
        # Test when max_discount_amount is greater than the price
        self.product.max_discount_amount = 200
        self.assertEqual(self.product.discounted_price, 0)  # Discount should equal the price, resulting in 0 discounted price
