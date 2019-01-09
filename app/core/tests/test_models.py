from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@email.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email successful"""
        email = 'test@email.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password, (password))

    def test_new_user_email_normalized(self):
        """Test the new email for a user is normalized"""
        email = 'test@EMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_category_str(self):
        """Test the category string representation"""
        category = models.Category.objects.create(
            user=sample_user(),
            name='Sculpture'
        )

        self.assertEqual(str(category), category.name)

    def test_work_str(self):
        """Test the work string representation"""
        work = models.Work.objects.create(
            user=sample_user(),
            title='Fountain of Wisdom',
        )

        self.assertEqual(str(work), work.title)

    @patch('uuid.uuid4')
    def test_work_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.work_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/work/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
