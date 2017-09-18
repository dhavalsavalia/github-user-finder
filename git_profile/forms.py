from django import forms
from git_profile.models import Search


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = '__all__'
