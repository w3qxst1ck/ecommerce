from .models import Order


def product_count(request):
    if request.user.is_authenticated:
        result = 0
        order = Order.objects.filter(user=request.user, ordered=False)
        if order.exists():
            for item in order[0].items.all():
                result += item.quantity
        return {'items_in_cart': result}









