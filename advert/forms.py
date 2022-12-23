from django import forms
from captcha.fields import CaptchaField

from .models import SubRubric, SuperRubric, Advert, AdditionalImage, Comment


class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(),
                                          empty_label=None,
                                          label='Super Rubric',
                                          required=True)

    class Meta:
        model = SubRubric
        fields = '__all__'


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=32, required=False, label='')


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


AIFormSet = forms.inlineformset_factory(Advert, AdditionalImage, fields='__all__')


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'advert': forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Enter text from the picture',
                           error_messages={'invalid': 'Wrong text'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'advert': forms.HiddenInput}
