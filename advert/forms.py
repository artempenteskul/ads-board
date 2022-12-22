from django import forms

from .models import SubRubric, SuperRubric, Advert, AdditionalImage


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
