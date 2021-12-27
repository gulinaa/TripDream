from django.urls import path

from main.views import DestinationsListView, DestinationDetailsView, CreateDestinationView, UpdateDestinationView, \
    DeleteDestinationView, SearchResultsView

urlpatterns = [
    path('', DestinationsListView.as_view(), name='destination-list'),
    path('<int:pk>/', DestinationDetailsView.as_view(), name='destination-details'),
    path('create/', CreateDestinationView.as_view(), name='create-destination'),
    path('update/<int:pk>/', UpdateDestinationView.as_view(), name='update-destination'),
    path('delete/<int:pk>/', DeleteDestinationView.as_view(), name='delete-destination'),
    path('search/', SearchResultsView.as_view(), name='search'),
]
