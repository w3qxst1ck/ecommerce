from django.urls import path

from core.views import item_list, item_detail, add_to_cart, cart_list, cart_delete_item, \
    cart_delete_single_item

urlpatterns = [
    path('', item_list, name='home-page'),
    path('order_by/<str:ordering_obj>', item_list, name='order-by'),
    path('cart/', cart_list, name='cart-page'),
    path('delete_from_cart/<slug>/', cart_delete_item, name='delete-from-cart'),
    path('delete_from_cart_single_item/<slug>/', cart_delete_single_item, name='delete-from-cart-single-item'),
    path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add_to_cart/<slug>/<str:cart>/', add_to_cart, name='add-to-cart-from-cart'),
    path('category/<str:category_slug>/', item_list, name='home-page-category'),
    path('<str:category_slug>/<str:item_slug>/', item_detail, name='item-detail'),

]