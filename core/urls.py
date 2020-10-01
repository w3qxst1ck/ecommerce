from django.urls import path

from core.views import item_list, item_detail, add_to_cart

urlpatterns = [
    path('', item_list, name='home-page'),
    path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('<str:category_slug>/<str:item_slug>/', item_detail, name='item-detail'),

]