from django import forms
from .models import Paintings


class AddPainting(forms.ModelForm):
    class Meta:
        model = Paintings
        fields = ('painting', 'title', 'description')
        widgets = {
            'description': forms.TextInput(
                attrs={'placeholder': 'Write how the painting made you feel...or not😉😉'}),
            'title': forms.TextInput(
                attrs={'placeholder': 'Give the painting a title...'})
            }