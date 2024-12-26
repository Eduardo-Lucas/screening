from rest_framework.permissions import BasePermission

class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.profile.user_type == 'candidate'
    
class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.profile.user_type == 'recruiter'
