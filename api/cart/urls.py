from django.urls import path

from api.cart.views import RmoveItemFromCartView, AddToCartView, CartItemsView

urlpatterns = [
    path('remove/<int:pk>/', RmoveItemFromCartView.as_view()),
    path('<int:pk>/', AddToCartView.as_view()),
    path('', CartItemsView.as_view()),
]

