from rest_framework import generics, permissions, views, response, viewsets
from django.utils import timezone

from api.serializers import ItemSerializer, ItemDetailSerializer, CartSerializser, WishListSerializer
from core.models import Item, Order, OrderItem, WishItem


class ListItemView(generics.ListAPIView):
    """ Item list
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailView(generics.RetrieveAPIView):
    """ Item detail
    """
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer


class CartItemsView(generics.ListAPIView):
    """ Items in cart
    """
    serializer_class = CartSerializser
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, ordered=False)


class AddToCartView(views.APIView):
    """ Add item to cart and delete single item from cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return response.Response(status=404)
        order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                return response.Response(status=201)
            else:
                order.items.add(order_item)
                return response.Response(status=201)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            return response.Response(status=201)

    def delete(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return response.Response(status=404)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
                if order_item.quantity == 1:
                    order.items.remove(order_item)
                    order_item.delete()
                    return response.Response(204)
                else:
                    order_item.quantity -= 1
                    order_item.save()
                return response.Response(204)
            else:
                response.Response(400)
        else:
            response.Response(400)


class RmoveItemFromCartView(views.APIView):
    """ Remove item from cart
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            item = Item.objects.get(id=pk)
        except Item.DoesNotExist:
            return response.Response(status=404)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
                order.items.remove(order_item)
                order_item.delete()
                return response.Response(status=204)
            else:
                return response.Response(status=400)
        else:
            return response.Response(status=400)


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

