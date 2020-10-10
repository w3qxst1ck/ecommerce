from .models import Order


def product_count(request):
    if request.user.is_authenticated:
        result = 0
        if Order.objects.filter(user=request.user, ordered=False).exists():
            order = Order.objects.filter(user=request.user, ordered=False)
            for item in order[0].items.all():
                result += item.quantity
        return {'items_in_cart': result}
    return {'items_in_cart': 0}








