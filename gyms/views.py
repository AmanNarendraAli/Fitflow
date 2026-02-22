from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .models import Room
from .forms import RoomForm
from accounts.utils import GymQuerySetMixin, role_required
from django.utils.decorators import method_decorator
# Create your views here.

class RoomListView(GymQuerySetMixin, ListView):
    model = Room
    template_name = 'room_list.html'
    context_object_name = 'rooms'

@method_decorator(role_required(['OWNER', 'STAFF']), name='dispatch')
class RoomCreateView(GymQuerySetMixin, CreateView):
    form_class = RoomForm
    template_name = 'room_form.html'
    success_url = reverse_lazy('room_list') #django's class-based version of render
    def form_valid(self, form):
        form.instance.gym = self.request.user.gym #sets gym in form to user's signed-in gym
        return super().form_valid(form) #automatically saves the form if valid

@method_decorator(role_required(['OWNER']), name='dispatch')
class RoomDeleteView(GymQuerySetMixin, DeleteView):
    model = Room
    template_name = 'room_confirm_delete.html'
    success_url = reverse_lazy('room_list')
    