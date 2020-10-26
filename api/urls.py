from django.urls import path

from api.views import ListItemView, ItemDetailView, CartItemsView, AddToCartView, RmoveItemFromCartView

urlpatterns = [
    path('items/', ListItemView.as_view()),
    path('items/<int:pk>/', ItemDetailView.as_view()),
    path('cart/remove/<int:pk>/', RmoveItemFromCartView.as_view()),
    path('cart/<int:pk>/', AddToCartView.as_view()),
    path('cart/', CartItemsView.as_view()),
]