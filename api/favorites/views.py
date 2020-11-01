from rest_framework import generics, permissions, views, response, viewsets

from api.favorites.serializers import WishListSerializer
from api.items.serializers import ItemDetailSerializer
from core.models import Item, WishItem


# APIView for Wish list
class ListWishItemsView(generics.ListAPIView):
    """ List wish items
    """
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishItem.objects.filter(user=self.request.user).order_by('-adding_date')


class DetailWishItemView(views.APIView):
    """ Detail view, add and delete wish items
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            instance = WishItem.objects.get(user=request.user, item_id=pk).item
        except WishItem.DoesNotExist:
            return response.Response(status=404)
        serializer = ItemDetailSerializer(instance)
        return response.Response(serializer.data)

    def post(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return response.Response(status=404)

        if WishItem.objects.filter(user=request.user, item=item).exists():
            return response.Response(status=400)
        else:
            WishItem.objects.create(user=request.user, item=item)
            return response.Response(204)

    def delete(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return response.Response(status=404)

        if WishItem.objects.filter(user=request.user, item=item).exists():
            wish_item = WishItem.objects.get(user=request.user, item=item)
            wish_item.delete()
            return response.Response(status=204)
        else:
            return response.Response(400)


# Viewset for wish list
class FavoritesViewSet(viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishItem.objects.filter(user=self.request.user).order_by('-adding_date')

    def create(self, request, *args, **kwargs):
        try:
            item = Item.objects.get(id=kwargs.get('pk'))
        except Item.DoesNotExist:
            return response.Response(status=404)

        if WishItem.objects.filter(user=request.user, item=item).exists():
            return response.Response(status=400)
        else:
            WishItem.objects.create(user=request.user, item=item)
            return response.Response(204)

    def destroy(self, request, *args, **kwargs):
        try:
            item = Item.objects.get(id=kwargs.get('pk'))
        except Item.DoesNotExist:
            return response.Response(status=404)

        if WishItem.objects.filter(user=request.user, item=item).exists():
            wish_item = WishItem.objects.get(user=request.user, item=item)
            wish_item.delete()
            return response.Response(status=204)
        else:
            return response.Response(400)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = WishItem.objects.get(user=request.user, item_id=kwargs.get('pk')).item
        except WishItem.DoesNotExist:
            return response.Response(status=404)
        serializer = ItemDetailSerializer(instance)
        return response.Response(serializer.data)
