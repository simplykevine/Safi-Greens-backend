from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    """
    Allows access only to users with user_type 'customer'.
    """
    message = "Only customers are allowed to perform this action."
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) == 'customer'

class IsVendor(BasePermission):
    """
    Allows access only to users with user_type 'vendor'.
    """
    message = "Only vendors are allowed to perform this action."
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) == 'vendor'

class IsAdminUserType(BasePermission):
    """
    Allows access only to users with user_type 'admin'.
    """
    message = "Only admins are allowed to perform this action."
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) == 'admin'

class IsVendorOrAdmin(BasePermission):
    """
    Allows access only to users with user_type 'vendor' or 'admin'.
    """
    message = "Only vendors or admins are allowed to perform this action."
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) in ['vendor', 'admin']

class IsCustomerOrAdmin(BasePermission):
    """
    Allows access only to users with user_type 'customer' or 'admin'.
    """
    message = "Only customers or admins are allowed to perform this action."
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) in ['customer', 'admin']

class IsCustomerOrVendorOrAdmin(BasePermission):
    """
    Allows access to customers, vendors, or admins.
    """
    message = "Only customers, vendors, or admins are allowed to perform this action."
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'user_type', None) in ['customer', 'vendor', 'admin']