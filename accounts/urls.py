from django.urls import path
from . import views
urlpatterns = [
    path('register/owner/', views.register_owner, name='register_owner'),
]