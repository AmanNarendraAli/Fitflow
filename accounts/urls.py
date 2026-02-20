from django.urls import path
from django.http import HttpResponse 
from . import views
urlpatterns = [
    path('register/owner/', views.register_owner, name='register_owner'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('join/',views.join_gym,name='join_gym'),
    path('userprofile/',views.MemberProfileView,name='userprof'),
    path('trainerprofile/',views.TrainerProfileView,name='trainerprof'),
]