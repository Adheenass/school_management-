from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnly(BasePermission):
    """
    Custom permission to allow only Admins to manage OfficeStaff and Librarian.
    """

    def has_permission(self, request, view):
       
        if request.user.role == 'admin':
            return True

        # Deny access for others
        return False
