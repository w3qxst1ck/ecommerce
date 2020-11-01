from rest_framework import serializers

from core.models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'title', 'slug', 'category', 'price', 'discount_price')


class ItemDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'title', 'slug', 'category', 'price', 'discount_price', 'description',
                  'created', 'image', 'item_images')




