from rest_framework import generics

from api.serializers import ItemSerializer, ItemDetailSerializer
from core.models import Item


class ListItemView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer