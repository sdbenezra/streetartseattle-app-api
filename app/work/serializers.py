from rest_framework import serializers

from core.models import Tag, Category, Work


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category objects"""

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class WorkSerializer(serializers.ModelSerializer):
    """Serializer for work objects"""
    category = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Work
        fields = (
            'id', 'title', 'artist', 'category', 'about',
            'media', 'measurements', 'date', 'location',
            'address', 'lat', 'long', 'tags'
            )
        read_only_fields = ('id',)
