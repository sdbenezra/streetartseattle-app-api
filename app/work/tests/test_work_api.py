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
    """Test work API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )

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
