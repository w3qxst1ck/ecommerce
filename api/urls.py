from django.urls import path

from api.views import ListItemView, ItemDetailView, CartItemsView, AddToCartView, \
    RmoveItemFromCartView, ListWishItemsView, DetailWishItemView, FavoritesViewSet, DetailWishItemView

urlpatterns = [
    path('items/', ListItemView.as_view()),
    path('items/<int:pk>/', ItemDetailView.as_view()),
    path('cart/remove/<int:pk>/', RmoveItemFromCartView.as_view()),
    path('cart/<int:pk>/', AddToCartView.as_view()),
    path('cart/', CartItemsView.as_view()),
    # path('favorites/<int:pk>/', DetailWishItemView.as_view()),
    # path('favorites/', ListWishItemsView.as_view()),
    path('favorites/', FavoritesViewSet.as_view({'get': 'list'})),
    path('favorites/<int:pk>/', FavoritesViewSet.as_view({'get': 'retrieve', 'post': 'create',
                                                          'delete': 'destroy'})),
]