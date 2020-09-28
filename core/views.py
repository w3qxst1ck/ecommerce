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
