from django.urls import path

from api.items.views import ListItemView, ItemDetailView

urlpatterns = [
    path('', ListItemView.as_view()),
    path('<int:pk>/', ItemDetailView.as_view()),
]
