from django.urls import path

from core.views import item_list, item_detail, add_to_cart, category_item, cart_list, cart_delete_item

urlpatterns = [
    path('', item_list, name='home-page'),
    path('cart/', cart_list, name='cart-page'),
    path('delete_from_cart/<slug>/', cart_delete_item, name='delete-from-cart'),
    path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('category/<str:category_slug>/', category_item, name='category-items'),
    path('<str:category_slug>/<str:item_slug>/', item_detail, name='item-detail'),

]