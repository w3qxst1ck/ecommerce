from django.urls import path

from api.items.views import ListItemView, ItemDetailView, CategoryListView, CategoryDetailView

urlpatterns = [
    path('', ListItemView.as_view()),
    path('<int:pk>/', ItemDetailView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),

]
