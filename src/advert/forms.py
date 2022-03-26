from django import forms

from .models import CustomUser


class ChangeUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')
