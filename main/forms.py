from django import forms
from .models import Paintings, PaintTries


class AddPainting(forms.ModelForm):
    class Meta:
        model = Paintings
        fields = ('painting', 'title', 'tags')
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Give the painting a title...'}),
            'tags': forms.TextInput(
                attrs={'placeholder': 'figure-painting, portrait, landscape'})
            }


class AddPaintingTry(forms.ModelForm):
    class Meta:
        model = PaintTries
        fields = ('tries',)

