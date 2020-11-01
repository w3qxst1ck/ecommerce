from rest_framework import serializers

from core.models import Order, OrderItem


class CartItemsSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(slug_field='title', read_only=True)
    item_id = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = OrderItem
        fields = ('item_id', 'item', 'quantity')


class CartSerializser(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    items = CartItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'items', 'start_date', 'ordered')


# class AddToCartSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Order
#         fields = ('items', )



