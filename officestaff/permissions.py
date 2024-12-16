from rest_framework.permissions import BasePermission

class IsOfficeStaff(BasePermission):
    """
    Custom permission to allow only Admins to manage OfficeStaff and Librarian.
    """

    def has_permission(self, request, view):
       
        if request.user.role == 'officestaff':
            return True

        # Deny access for others
        return False
