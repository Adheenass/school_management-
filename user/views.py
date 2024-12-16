from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import UserSerializer
from user.models import User
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from user.permission import IsAdminUserOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class LoginView(APIView):
    def post(self, request):
        # Get email and password from the request
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Fetch the user using the email
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):  # Check if passwords match
                # Check if the user is an admin
                if user.role == 'admin':
                    # Generate JWT token for the admin user
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                    }, status=200)
                else:
                    return Response({'detail': 'User is not an admin.'}, status=403)
            else:
                return Response({'detail': 'Invalid credentials or unauthorized user.'}, status=401)

        return Response(serializer.errors, status=400)

class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Delete the user's token
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class UserCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAdminUserOrReadOnly] 
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve details of a specific user.
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        """
        Update a user.
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(User, data=request.data, partial=True)  # partial=True for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a user.
        """
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)