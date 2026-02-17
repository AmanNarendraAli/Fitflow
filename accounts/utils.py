from django.core.exceptions import PermissionDenied
from functools import wraps
from django.shortcuts import redirect

class GymQuerySetMixin:
    def get_queryset(self):
        # 1. Start with the standard list (e.g., all Bookings)
        qs = super().get_queryset()
        
        # 2. Chop that list down to ONLY this user's gym
        # This prevents Gym A from seeing Gym B's data
        return qs.filter(gym=self.request.user.gym)

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func) #we need to write the decorator this way because we want to accept arguments (acceptable roles)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
