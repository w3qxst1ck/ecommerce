from django.urls import path

from api.cart.views import RmoveItemFromCartView, DetailCartItemView, ListCartItemsView

urlpatterns = [
    path('remove/<int:pk>/', RmoveItemFromCartView.as_view()),
    path('<int:pk>/', DetailCartItemView.as_view()),
    path('', ListCartItemsView.as_view()),
]

