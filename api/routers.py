from django.urls import path, include


urlpatterns = [
    path('cart/', include('api.cart.urls')),
    path('favorites/', include('api.favorites.urls')),
    path('items/', include('api.items.urls')),

]