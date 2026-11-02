from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    
    def has_permission(self,req,view):
        return{
            req.user
            and req.user.is_authenticated
            and req.user.role=="admin"
        }