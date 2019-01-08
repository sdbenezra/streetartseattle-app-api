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
    category = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='name'

    )
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Work
        fields = (
            'id', 'title', 'artist', 'category', 'about',
            'media', 'measurements', 'date', 'location',
            'address', 'lat', 'long', 'tags', 'image'
            )
        read_only_fields = ('id',)


class WorkDetailSerializer(WorkSerializer):
    """Serialize a work detail"""
    category = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class WorkImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to works"""

    class Meta:
        model = Work
        fields = ('id', 'image')
        read_only_fields = ('id',)
