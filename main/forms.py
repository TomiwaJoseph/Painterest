from django import forms
from .models import Paintings


class AddPainting(forms.ModelForm):
    class Meta:
        model = Paintings
        fields = ('painting', 'title', 'feel')
        widgets = {
            'feel': forms.TextInput(
                attrs={'placeholder': 'Write how the painting make you feel...'}),
            'title': forms.TextInput(
                attrs={'placeholder': 'Give the painting a title...'})
            }