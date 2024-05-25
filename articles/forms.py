from django import forms
from django.contrib.auth.models import User

from .models import Article

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
class AddPageForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('article_title', 'article_text', 'status', 'tags')
        widgets = {
            'article_title': forms.TextInput(attrs={'class': 'form-control'}),
            'article_text': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddPageForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required = False

class SearchForm(forms.Form):
        query = forms.CharField(label='Введите запрос', widget=forms.TextInput(attrs={'class': 'form-control'}))
