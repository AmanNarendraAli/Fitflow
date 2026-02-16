from django import forms
from django.contrib.auth.forms import UserCreationForm #to inherit the default user creation form but with our Model modifications
from .models import Gym, User

class GymForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ['name', 'address', 'phone', 'email', 'code']

class OwnerSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']



