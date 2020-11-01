from rest_framework import serializers

from api.items.serializers import ItemDetailSerializer
from core.models import WishItem


class WishListSerializer(serializers.ModelSerializer):
    item = ItemDetailSerializer()

    class Meta:
        model = WishItem
        fields = ('item', 'adding_date')


