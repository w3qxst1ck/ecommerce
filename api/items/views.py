from rest_framework import generics
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from api.items.serializers import ItemListSerializer, ItemDetailSerializer, CategorySerializer, CategoryDetailSerializer
from api.items.service import ItemFilter
from core.models import Item, Category


class ListItemView(generics.ListAPIView):
    """ Item list
    """
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = ItemFilter
    search_fields = ['title', 'description', 'category__title']
    ordering_fields = ['title', 'price', 'category__title']


class ItemDetailView(generics.RetrieveAPIView):
    """ Item detail
    """
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class CategoryListView(generics.ListAPIView):
    """ Categories list with items_count
    """
    queryset = Category.objects.all().order_by('id').annotate(items_count=Count('category_items'))
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    """ Category detail view
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategoryDetailSerializer