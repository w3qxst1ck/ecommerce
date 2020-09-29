from django.shortcuts import render

from core.models import Item, Category


def item_list(request):
    items = Item.objects.all().order_by('category')
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)


def item_detail(request, item_slug, category_slug):
    item = Item.objects.get(slug=item_slug)
    category = Category.objects.get(slug=category_slug)
    context = {
        'item': item,
        'category': category
    }
    return render(request, 'core/item_detail.html', context)

