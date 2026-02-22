from django import forms
from django.contrib.auth.forms import UserCreationForm #to inherit the default user creation form but with our Model modifications
from .models import Gym, User, TrainerProfile, MemberProfile
from django.forms import modelformset_factory

MemberRoleFormSet = modelformset_factory(User,fields=['role'],extra=0,widgets={'role': forms.Select(attrs={'class': 'form-control'})}) #we don't want blank rows, hence the extra = 0. this formset class allows us to manage multiple users at once
class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ['name', 'address', 'phone', 'email']

class OwnerSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

class JoinGymForm(UserCreationForm):
    gym_code = forms.CharField(max_length=6, help_text="Enter the 6-character code given by your gym owner.")
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    def clean_gym_code(self):
        code = self.cleaned_data.get('gym_code')
        try:
            gym = Gym.objects.get(code=code) #checking if the gym exists
        except Gym.DoesNotExist:
            raise forms.ValidationError("Invalid gym code.")
        return gym
    
    def save(self, commit = True): # we have to override the basic save function. This is because the basic save function only knows what's in the Meta class, and if we put gym and role in the meta class, the user would get a dropdown showing all gyms and would be able to pick their role. 
        user = super().save(commit=False)
        user.gym = self.cleaned_data['gym_code']
        user.role = User.MEMBER
        if commit:
            user.save()
        return user

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['bio', 'specialties']

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['phone', 'emergency_contact']