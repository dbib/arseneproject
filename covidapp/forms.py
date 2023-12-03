# covidapp/forms.py
from django import forms
from .models import User

# Formulaire pour la creation du compte des utilisateurs
class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }


# Formulaire de le login des utilisateurs
class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)