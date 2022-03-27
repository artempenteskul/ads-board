from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import CustomUser
from .apps import user_registered


class ChangeUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text=password_validation._password_validators_help_text_html(),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        help_text='Enter same password again',
        label='Confirm password'
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        if password:
            password_validation.validate_password(password)
        return password

    def clean(self):
        if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data and self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError({'confirm_password': 'Passwords should match'}, code='password_mismatch')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password', 'send_messages')
