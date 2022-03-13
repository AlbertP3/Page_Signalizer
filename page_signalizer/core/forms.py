from django import forms
from .models import Connection_Spec

class Connection_Spec_CreationForm(forms.ModelForm):
    class Meta:
        model = Connection_Spec
        fields = ['name', 'url', 'seq', 'interval_seconds']