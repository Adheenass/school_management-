from django.urls import path
from .views import FeesHistoryAPIView,LibraryHistoryAPIView

urlpatterns = [
    path('fees-history/', FeesHistoryAPIView.as_view(), name='fees-history'),
    path('fees-history/<int:pk>/', FeesHistoryAPIView.as_view(), name='fees-history-detail'),
     # Endpoint for listing and creating borrowing records
    path('library/', LibraryHistoryAPIView.as_view(), name='library-list-create'),

    # Endpoint for retrieving, updating, or deleting a specific record
    path('library/<int:pk>/', LibraryHistoryAPIView.as_view(), name='library-detail'),
]
