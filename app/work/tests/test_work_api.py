from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Work, Tag, Category

from work.serializers import WorkSerializer, WorkDetailSerializer


WORKS_URL = reverse('work:work-list')


def detail_url(work_id):
    """Return work detail URL"""
    return reverse('work:work-detail', args=[work_id])


def sample_tag(user, name='kid-friendly'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_category(user, name='Sculpture'):
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

        works = Work.objects.all().order_by('id')
        serializer = WorkSerializer(works, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_view_work_detail(self):
        """Test viewing a detail of a work"""
        work = sample_work(user=self.user)
        work.tags.add(sample_tag(user=self.user))
        work.category.add(sample_category(user=self.user))

        url = detail_url(work.id)
        res = self.client.get(url)

        serializer = WorkDetailSerializer(work)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_work(self):
        """Test creating a work"""
        payload = {
            'user': self.user,
            'title': 'Fountain of Wisdom',
            'artist': 'George Tsutakawa'
        }
        res = self.client.post(WORKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        work = Work.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(work, key))

    def test_create_works_with_tags(self):
        """Test creating a work with tags"""
        tag1 = sample_tag(user=self.user, name='Kid Friendly')
        tag2 = sample_tag(user=self.user, name='Georgetown')
        payload = {
            'title': 'Fountain of Wisdom',
            'tags': [tag1.id, tag2.id],
        }
        res = self.client.post(WORKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        work = Work.objects.get(id=res.data['id'])
        tags = work.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_work_with_category(self):
        """Test create work with category"""
        category1 = sample_category(user=self.user, name='Sculpture')
        category2 = sample_category(user=self.user, name='Public')
        payload = {
            'title': 'Fountain of Wisdom',
            'category': [category1.id, category2.id]
        }
        res = self.client.post(WORKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        work = Work.objects.get(id=res.data['id'])
        categories = work.category.all()
        self.assertEqual(categories.count(), 2)
        self.assertIn(category1, categories)
        self.assertIn(category2, categories)
