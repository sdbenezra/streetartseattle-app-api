from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

from core.models import Category, Work

from django.db.models import Q

from work import serializers

import re


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

    def _get_query(self, query_string):
        query = None
        findterms = re.compile(r'"([^"]+)"|(\S+)').findall
        normspace = re.compile(r'\s{2,}').sub
        terms = [normspace('', (t[0] or t[1]).strip())
                 for t in findterms(query_string)]
        for term in terms:
            or_query = None
            for field_name in ['category__name', 'title',
                               'artist', 'location']:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
                if query is None:
                    query = or_query
                else:
                    query = query | or_query
        return query

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve list of works"""
        search_term = self.request.query_params.get('search')
        found_entries = None
        if search_term:
            entry_query = self._get_query(search_term)
            found_entries = self.queryset.filter(entry_query)
            return found_entries
        else:
            return self.queryset

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
