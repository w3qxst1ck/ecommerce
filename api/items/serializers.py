from rest_framework import serializers

from core.models import Item, Category


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


class CategorySerializer(serializers.ModelSerializer):
    items_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'items_count')


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_items = ItemSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'category_items')






