from django.urls import path

from core.views import item_list, item_detail

urlpatterns = [
    path('', item_list, name='home-page'),
    path('<str:category_slug>/<str:item_slug>/', item_detail, name='item-detail'),
]