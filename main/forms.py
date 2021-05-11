from django import forms
from .models import Paintings, PaintTries


class AddPainting(forms.ModelForm):
    class Meta:
        model = Paintings
        fields = ('painting', 'title', 'description', 'tags')
        widgets = {
            'description': forms.TextInput(
                attrs={'placeholder': 'Write how the painting made you feel...or not😉😉'}),
            'title': forms.TextInput(
                attrs={'placeholder': 'Give the painting a title...'}),
            'tags': forms.TextInput(
                attrs={'placeholder': 'figure-painting, portrait, landscape'})
            }


class AddPaintingTry(forms.ModelForm):
    class Meta:
        model = PaintTries
        fields = ('tries',)

