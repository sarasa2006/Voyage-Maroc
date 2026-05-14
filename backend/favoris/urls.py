from django.urls import path
from .views import FavoriListView, AddFavoriView, RemoveFavoriView

urlpatterns = [
    path('', FavoriListView.as_view(), name='favori_list'),
    path('ajouter/<int:pk>/', AddFavoriView.as_view(), name='favori_add'),
    path('supprimer/<int:pk>/', RemoveFavoriView.as_view(), name='favori_remove'),
]
