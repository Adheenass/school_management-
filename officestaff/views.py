from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import FeesHistory,LibraryHistory
from .serializers import FeesHistorySerializer,LibraryHistorySerializer
from .permissions import IsOfficeStaff
from rest_framework_simplejwt.authentication import JWTAuthentication

class FeesHistoryAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsOfficeStaff]
    def get(self, request, pk=None):
        if pk:
            # Retrieve a specific record
            fees_history = get_object_or_404(FeesHistory, pk=pk)
            serializer = FeesHistorySerializer(fees_history)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Retrieve all records
        fees_history = FeesHistory.objects.all()
        serializer = FeesHistorySerializer(fees_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeesHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        fees_history = get_object_or_404(FeesHistory, pk=pk)
        serializer = FeesHistorySerializer(fees_history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        fees_history = get_object_or_404(FeesHistory, pk=pk)
        fees_history.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




class LibraryHistoryAPIView(APIView):
    """
    Handle list, create, retrieve, update, and delete operations for LibraryHistory.
    """

    def get(self, request, pk=None, *args, **kwargs):
        """
        GET:
        - List all borrowing records (if `pk` is not provided)
        - Retrieve a single record (if `pk` is provided)
        """
        if pk:
            library_history = get_object_or_404(LibraryHistory, pk=pk)
            serializer = LibraryHistorySerializer(library_history)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            library_histories = LibraryHistory.objects.all()
            serializer = LibraryHistorySerializer(library_histories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        POST:
        Create a new borrowing record.
        """
        serializer = LibraryHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        """
        PUT:
        Update an existing borrowing record.
        """
        library_history = get_object_or_404(LibraryHistory, pk=pk)
        serializer = LibraryHistorySerializer(library_history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        DELETE:
        Delete a borrowing record.
        """
        library_history = get_object_or_404(LibraryHistory, pk=pk)
        library_history.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
