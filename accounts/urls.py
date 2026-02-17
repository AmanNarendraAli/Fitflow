from django.urls import path
from django.http import HttpResponse 
from . import views
urlpatterns = [
    path('register/owner/', views.register_owner, name='register_owner'),
    path('dashboard/', lambda r: HttpResponse("Success! Data is saved."), name='dashboard'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('join/',views.join_gym,name='join_gym'),
]