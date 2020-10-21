from rest_framework import serializers

from core.models import Item, ItemImage


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'title', 'slug', 'category', 'price', 'discount_price')


class FilterImagesSerializer(serializers.ListSerializer):
    def to_representation(self, instance, **kwargs):
        instance = instance.filter(item_id=kwargs['pk'])
        return super().to_representation(instance)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilterImagesSerializer
        model = ItemImage
        fields = ('id', 'image')


class ItemDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'title', 'slug', 'category', 'price', 'discount_price', 'description',
                  'created', 'image', 'images')
