from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from core.models import Item, Category, OrderItem, Order


current_path = ''


def item_list(request):
    items = Item.objects.all().order_by('category')
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
    }
    global current_path
    current_path = request.path
    return render(request, 'core/home.html', context)


def item_detail(request, item_slug, category_slug):
    item = Item.objects.get(slug=item_slug)
    category = Category.objects.get(slug=category_slug)
    context = {
        'item': item,
        'category': category
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
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            return cart_add_redirect(request, item)
        else:
            order.items.add(order_item)
            return cart_add_redirect(request, item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return cart_add_redirect(request, item)


def category_item(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    items = Item.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
        'category': category
    }
    return render(request, 'core/category_items.html', context)


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
            messages.info(request, f'Product has been delete from order')
            return redirect('cart-page')
        else:
            messages.info(request, f'This product in your cart')
            return redirect('cart-page')
    else:
        messages.info(request, f'you havent got active order')
        return redirect('cart-page')


@login_required
def cart_list(request):
    order = Order.objects.filter(user=request.user, ordered=False)
    items = order[0].items.all()
    print(items)
    context = {
        'items': items,
        'order': order
    }
    return render(request, 'core/cart.html', context)


