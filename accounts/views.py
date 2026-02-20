from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth import login, logout
from .forms import GymForm, OwnerSignupForm, JoinGymForm, MemberProfileForm, TrainerProfileForm
from .models import User
from .utils import role_required
from django.contrib.auth.forms import AuthenticationForm
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

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
        
def join_gym(request):
    if request.method == 'POST':
        form = JoinGymForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log them in immediately
            return redirect('dashboard')
    else:
        form = JoinGymForm()
    return render(request, 'join_gym.html', {'form': form})

@login_required
@role_required(['OWNER', 'STAFF', 'TRAINER', 'MEMBER'])
def dashboard(request):
        gym = request.user.gym
        rooms_count = gym.rooms.count()
        members_count = User.objects.filter(gym=gym, role=User.MEMBER).count()
        trainers_count = User.objects.filter(gym=gym, role=User.TRAINER).count()
        return render(request, 'dashboard.html', {
            'gym': gym,
            'rooms_count': rooms_count,
            'members_count': members_count,
            'trainers_count': trainers_count
        })

@login_required
@role_required(['OWNER', 'STAFF', 'TRAINER', 'MEMBER'])
def TrainerProfileView(request):
    profile = request.user.trainer_profile
    if request.method=='POST':
        form = TrainerProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TrainerProfileForm(instance=profile)
    return render(request, 'trainer_profile.html', {'form': form})

@login_required
@role_required(['OWNER', 'STAFF', 'TRAINER', 'MEMBER'])
def MemberProfileView(request):
    profile = request.user.member_profile
    if request.method=='POST':
        form = MemberProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MemberProfileForm(instance=profile)
    return render(request, 'member_profile.html', {'form': form})