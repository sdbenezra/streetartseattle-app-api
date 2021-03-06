import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Work, Category

from work.serializers import WorkSerializer, WorkDetailSerializer


WORKS_URL = reverse('work:work-list')


def image_upload_url(work_id):
    """Return URL for work image upload"""
    return reverse('work:work-upload-image', args=[work_id])


def detail_url(work_id):
    """Return work detail URL"""
    return reverse('work:work-detail', args=[work_id])


def sample_category(user, name='Test Category1'):
    """Create and return a sample category"""
    return Category.objects.create(user=user, name=name)


def sample_work(user, **params):
    """Create and return a sample work"""
    defaults = {
        'title': 'Sample work',
    }
    defaults.update(params)

    return Work.objects.create(user=user, **defaults)


class PublicWorkApiTests(TestCase):
    """Test work API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_listing_of_works(self):
        """Test retrieving a list of works"""
        user2 = get_user_model().objects.create_user(
            'test2@email.com',
            'testpass2'
        )
        sample_work(user=user2)
        sample_work(user=self.user)

        res = self.client.get(WORKS_URL)

        works = Work.objects.all().order_by('-id')
        serializer = WorkSerializer(works, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_work_detail(self):
        """Test viewing a detail of a work"""
        work = sample_work(user=self.user)

        url = detail_url(work.id)
        res = self.client.get(url)

        serializer = WorkDetailSerializer(work)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_work(self):
        """Test creating a work"""
        payload = {
            'title': 'Fountain of Wisdom',
            'artist': 'George Tsutakawa'
        }
        res = self.client.post(WORKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        work = Work.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(work, key))

    def test_create_work_with_category(self):
        """Test create work with category"""
        category1 = sample_category(user=self.user, name='Test Category1')
        category2 = sample_category(user=self.user, name='Test Category2')
        payload = {
            'title': 'Fountain of Wisdom',
            'category': [category1.name, category2.name]
        }
        res = self.client.post(WORKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        work = Work.objects.get(id=res.data['id'])
        categories = work.category.all()
        self.assertEqual(categories.count(), 2)
        self.assertIn(category1, categories)
        self.assertIn(category2, categories)

    def test_partial_update_work(self):
        """Test updating a work with patch"""
        work = sample_work(user=self.user)

        payload = {'title': 'New Sample Title'}
        url = detail_url(work.id)
        self.client.patch(url, payload)

        work.refresh_from_db()
        self.assertEqual(work.title, payload['title'])

    def test_full_update_work(self):
        """Test updating work with put"""
        work = sample_work(user=self.user)
        payload = {
            'title': 'Another new title',
            'artist': 'New Artist'
        }
        url = detail_url(work.id)
        self.client.put(url, payload)

        work.refresh_from_db()
        self.assertEqual(work.title, payload['title'])
        self.assertEqual(work.artist, payload['artist'])


class WorkImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'email@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        self.work = sample_work(user=self.user)

    def tearDown(self):
        self.work.image.delete()

    def test_upload_image_to_work(self):
        """Test uploading an image to work"""
        url = image_upload_url(self.work.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.work.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.work.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.work.id)
        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class WorkSearchTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'email@email.com', 'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_search_works_by_category(self):
        """Test returning works with specific categories"""
        work1 = sample_work(user=self.user, title='World Union')
        work2 = sample_work(user=self.user, title='Mega Mile')
        work3 = sample_work(user=self.user, title='Hello Friends')
        category1 = sample_category(user=self.user, name='Test Category1')
        category2 = sample_category(user=self.user, name='Test Category2')
        work1.category.add(category1)
        work2.category.add(category2)

        res = self.client.get(
            WORKS_URL,
            {'search': f'{category1.name} {work2.title}'}
        )

        serializer1 = WorkSerializer(work1)
        serializer2 = WorkSerializer(work2)
        serializer3 = WorkSerializer(work3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
