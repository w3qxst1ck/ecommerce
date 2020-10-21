from django.urls import path

from api.views import ListItemView, ItemDetailView

urlpatterns = [
    path('items/', ListItemView.as_view()),
    path('items/<int:pk>/', ItemDetailView.as_view()),
]