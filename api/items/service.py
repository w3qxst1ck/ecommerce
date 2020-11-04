from django_filters import rest_framework as filters

from core.models import Item


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ItemFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    price = filters.RangeFilter()
    discount_price = filters.BooleanFilter(field_name='discount_price', lookup_expr='isnull')
    category = filters.CharFilter(field_name='category__title', lookup_expr='iexact')

    class Meta:
        model = Item
        fields = ['title', 'price', 'discount_price', 'category']

