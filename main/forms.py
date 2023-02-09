from django import forms
from .models import Paintings, PaintTries


class AddPainting(forms.ModelForm):
    painting = forms.ImageField(required=True)

    class Meta:
        model = Paintings
        fields = ('painting', 'title', 'artist_name', 'tags')
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Give the painting a title...'}),
            'tags': forms.TextInput(
                attrs={'placeholder': 'figure-painting, portrait, landscape'}),
            'artist_name': forms.TextInput(
                attrs={'placeholder': 'Tomiwa Joseph'})
        }


class AddPaintingTry(forms.ModelForm):
    class Meta:
        model = PaintTries
        fields = ('tries',)
