from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/create/', views.RoomCreateView.as_view(), name='room_create'),
]