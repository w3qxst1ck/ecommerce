from rest_framework import generics, permissions, views, response
from django.utils import timezone

from api.serializers import ItemSerializer, ItemDetailSerializer, CartSerializser, AddToCartSerializer
from core.models import Item, Order, OrderItem


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
