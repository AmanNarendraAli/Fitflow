class GymQuerySetMixin:
    def get_queryset(self):
        # 1. Start with the standard list (e.g., all Bookings)
        qs = super().get_queryset()
        
        # 2. Chop that list down to ONLY this user's gym
        # This prevents Gym A from seeing Gym B's data
        return qs.filter(gym=self.request.user.gym)