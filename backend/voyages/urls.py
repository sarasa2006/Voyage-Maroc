from django.urls import path
from .views import LieuListView, LieuDetailView, VoyageCreateView, VoyageDetailView, VoyageListView

urlpatterns = [
    path('', LieuListView.as_view(), name='lieux'),
    path('<int:pk>/', LieuDetailView.as_view(), name='lieu_detail'),
    path('voyage/nouveau/', VoyageCreateView.as_view(), name='voyage_create'),
    path('voyage/<int:pk>/', VoyageDetailView.as_view(), name='voyage_detail'),
    path('mes-voyages/', VoyageListView.as_view(), name='voyage_list'),
]