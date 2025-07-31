from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    message = "Only customers are allowed to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "user_type", None) == "customer"

class IsVendor(BasePermission):
    message = "Only vendors are allowed to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "user_type", None) == "vendor"

class IsAdminUserType(BasePermission):
    message = "Only admins are allowed to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "user_type", None) == "admin"

class IsVendorOrAdmin(BasePermission):
    message = "Only vendors or admins are allowed to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "user_type", None) in ["vendor", "admin"]

class IsCustomerOrAdmin(BasePermission):
    message = "Only customers or admins are allowed to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "user_type", None) in ["customer", "admin"]