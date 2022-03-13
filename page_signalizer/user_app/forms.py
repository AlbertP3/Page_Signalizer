from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Register_form(UserCreationForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1']


    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None