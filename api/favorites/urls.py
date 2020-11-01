from django.urls import path

from api.favorites.views import ListWishItemsView, DetailWishItemView, FavoritesViewSet

urlpatterns = [
    # path('<int:pk>/', DetailWishItemView.as_view()),
    # path('', ListWishItemsView.as_view()),
    path('', FavoritesViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', FavoritesViewSet.as_view({'get': 'retrieve', 'post': 'create',
                                                          'delete': 'destroy'})),
]

