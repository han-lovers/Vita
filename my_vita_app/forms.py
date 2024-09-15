from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReceiveImageForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'photo',}))

class UserForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer nombre'}),
                                 max_length=32)
    middle_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo nombre'}),
                                 max_length=32)
    paternal_last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido paterno'}),
                                 max_length=32)
    maternal_last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido materno'}),
                                 max_length=32)
    age = forms.IntegerField(required=True, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Su edad',}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Correo electronico'}), max_length=64)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repita la contraseña'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields =  ('first_name', 'middle_name', 'paternal_last_name', 'maternal_last_name', 'age', 'email', 'password1', 'password2')