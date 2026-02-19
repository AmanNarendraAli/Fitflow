from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Yoga Studio'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Max capacity'
            }),
        }
    