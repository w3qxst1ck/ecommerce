from django.urls import path

from core.views import item_list, item_detail, add_to_cart, cart_list, cart_delete_item, \
    cart_delete_single_item, wish_list, add_to_wish_list, remove_from_wish_list, remove_from_wish_list_in_list

urlpatterns = [
    path('', item_list, name='home-page'),
    path('cart/', cart_list, name='cart-page'),
    path('wish_list/', wish_list, name='wish-list'),
    path('delete_from_cart/<slug>/', cart_delete_item, name='delete-from-cart'),
    path('delete_from_cart_single_item/<slug>/', cart_delete_single_item, name='delete-from-cart-single-item'),
    path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add_to_cart/<slug>/<str:cart>/', add_to_cart, name='add-to-cart-from-cart'),
    path('category/<str:category_slug>/', item_list, name='home-page-category'),
    path('add_to_wish_list/<str:item_slug>/', add_to_wish_list, name='add-to-wish-list'),
    path('remove_from_wish_list/<str:item_slug>/', remove_from_wish_list, name='remove-from-wish-list'),
    path('remove_from_wish_list_in_list/<str:item_slug>/', remove_from_wish_list_in_list,
         name='remove-from-wish-list-in-list'),
    path('<str:category_slug>/<str:item_slug>/', item_detail, name='item-detail'),

]