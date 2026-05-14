from django import forms
from .models import Voyage


class VoyageForm(forms.ModelForm):
    """Formulaire de création d'un voyage à partir des favoris de l'utilisateur."""

    class Meta:
        model = Voyage
        fields = ['destination', 'duree', 'budget']
        widgets = {
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Marrakech, Fès, Agadir…',
            }),
            'duree': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de jours',
                'min': 1,
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Budget total en MAD',
                'min': 0,
                'step': '0.01',
            }),
        }
        labels = {
            'destination': 'Destination principale',
            'duree': 'Durée (jours)',
            'budget': 'Budget total (MAD)',
        }
