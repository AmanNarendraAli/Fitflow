from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth import login
from .forms import GymForm, OwnerSignupForm
from .models import User

# Create your views here.
@transaction.atomic
def register_owner(request):
    if request.method == 'POST':
        gym_form = GymForm(request.POST)
        owner_form = OwnerSignupForm(request.POST)
        if gym_form.is_valid() and owner_form.is_valid():
            gym = gym_form.save()
            owner = owner_form.save(commit=False)
            owner.gym = gym
            owner.role = User.OWNER
            owner.save()
            login(request,owner)
            return redirect('dashboard')
    else:
        gym_form = GymForm()
        owner_form = OwnerSignupForm()
        
    return render(request, 'register_owner.html', {
        'gym_form': gym_form,
        'user_form': owner_form
    })
