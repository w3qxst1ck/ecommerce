from django.urls import path

from core.views import item_list

urlpatterns = [
    path('', item_list, name='home-page'),
]