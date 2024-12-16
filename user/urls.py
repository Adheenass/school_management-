from django.urls import path
from .views import UserCreateAPIView, LoginView

urlpatterns = [
    path('create-user/', UserCreateAPIView.as_view(), name='api_create_user'),
    path('user/<int:pk>/', UserCreateAPIView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name='login'),
]
