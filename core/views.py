from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from core.models import Item, Category, OrderItem, Order, WishItem

current_path = ''


def item_list(request, category_slug=None, ordering_obj=None):
    categories = Category.objects.all()
    wish_items = []
    if request.user.is_authenticated:
        wish_items = [item.item for item in WishItem.objects.filter(user=request.user)]

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        items = Item.objects.filter(category=category)
    else:
        if ordering_obj:
            if ordering_obj == 'sale':
                items = [item for item in Item.objects.all() if item.discount_price]
            else:
                items = Item.objects.all().order_by(ordering_obj)
        else:
            items = Item.objects.all().order_by('category')
        category = None

    context = {
        'items': items,
        'categories': categories,
        'wish_items': wish_items,
        'category': category
    }
    global current_path
    current_path = request.path
    return render(request, 'core/home.html', context)


def item_detail(request, item_slug, category_slug):
    item = Item.objects.get(slug=item_slug)
    category = Category.objects.get(slug=category_slug)
    wish_items = []
    if request.user.is_authenticated:
        wish_items = [item.item for item in WishItem.objects.filter(user=request.user)]
    context = {
        'item': item,
        'category': category,
        'wish_items': wish_items,
    }
    global current_path
    current_path = request.path
    return render(request, 'core/item_detail.html', context)


def cart_add_redirect(request, item):
    messages.success(request, f'Product has been added to cart')
    if current_path == '/':
        return redirect('home-page')
    else:
        return redirect(item.get_absolute_url())


@login_required
def add_to_cart(request, slug, cart=None):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            if cart:
                return redirect('cart-page')
            else:
                return cart_add_redirect(request, item)
        else:
            order.items.add(order_item)
            if cart:
                return redirect('cart-page')
            else:
                return cart_add_redirect(request, item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        if cart:
            return redirect('cart-page')
        else:
            return cart_add_redirect(request, item)


@login_required
def cart_delete_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'Product has been deleted from order')
            return redirect('cart-page')
        else:
            messages.info(request, 'This product is not in your cart')
            return redirect('cart-page')
    else:
        messages.info(request, 'You haven\'t got active order')
        return redirect('cart-page')


@login_required
def cart_delete_single_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity == 1:
                order.items.remove(order_item)
                order_item.delete()
                messages.info(request, 'This item has been remove from your cart')
            else:
                order_item.quantity -= 1
                order_item.save()
            return redirect('cart-page')
        else:
            messages.info(request, 'This product is not in your cart')
            return redirect('cart-page')
    else:
        messages.info(request, 'You haven\'t got active order')
        return redirect('cart-page')


@login_required
def cart_list(request):
    order = Order.objects.filter(user=request.user, ordered=False)
    items = order[0].items.all().order_by('item__title')
    context = {
        'items': items,
        'order': order[0]
    }
    return render(request, 'core/cart.html', context)


@login_required
def wish_list(request):
    wish_items = WishItem.objects.filter(user=request.user).order_by('-adding_date')
    context = {
        'wish_items': wish_items,
    }
    return render(request, 'core/wish_list.html', context)


@login_required
def add_to_wish_list(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    WishItem.objects.create(user=request.user, item=item)
    messages.info(request, 'Item was added to your Favorites')
    return redirect('home-page')


@login_required
def remove_from_wish_list(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    wish_item = WishItem.objects.get(user=request.user, item=item)
    wish_item.delete()
    messages.warning(request, 'Item was removed form your Favorites')
    return redirect('home-page')


@login_required
def remove_from_wish_list_in_list(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    wish_item = WishItem.objects.get(user=request.user, item=item)
    wish_item.delete()
    messages.warning(request, 'Item was removed form your Favorites')
    return redirect('wish-list')


