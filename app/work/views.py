from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

from core.models import Category, Work

from work import serializers


class CategoryViewSet(viewsets.ModelViewSet):
    """Manage categories in the database"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        """Return list of categories, user authentication not required"""
        return self.queryset.order_by('name')


class WorkViewSet(viewsets.ModelViewSet):
    """Manage works in the database"""
    queryset = Work.objects.all()
    serializer_class = serializers.WorkSerializer

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve list of works"""
        categories = self.request.query_params.get('category')
        queryset = self.queryset

        if categories:
            category_ids = self._params_to_ints(categories)
            queryset = queryset.filter(category__id__in=category_ids)

        return queryset.order_by('id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.WorkDetailSerializer
        elif self.action == 'upload_image':
            return serializers.WorkImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a work"""
        work = self.get_object()
        serializer = self.get_serializer(
            work,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
