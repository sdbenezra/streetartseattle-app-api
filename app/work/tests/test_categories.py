from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

from work.serializers import CategorySerializer


CATEGORIES_URL = reverse('work:category-list')


class PublicCategoriesApiTests(TestCase):
    """Test the publicly available category API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_not_required(self):
        """Test that login is not required to access this endpoint"""
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_all_categories(self):
        """Test all categories listed for a user not logged in"""
        user1 = get_user_model().objects.create_user('email@test.com', 'pass1')
        user2 = get_user_model().objects.create_user('email2@tst.com', 'pass2')
        Category.objects.create(user=user1, name='Sculpture')
        Category.objects.create(user=user2, name='Mural')

        res = self.client.get(CATEGORIES_URL)

        categories = Category.objects.all().order_by('-name')
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 2)
