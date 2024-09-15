from django import forms
from .models import CustomUser

class ReceiveImageForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'photo',}))

class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer nombre'}),
                                 max_length=32)
    second_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo nombre'}),
                                 max_length=32)
    last_name_father = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido paterno'}),
                                 max_length=32)
    last_name_mother = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido materno'}),
                                 max_length=32)
    age = forms.IntegerField(required=True, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Su edad',}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Correo electronico'}), max_length=64)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repita la contraseña'}))
    
    class Meta:
        model = CustomUser
        fields =  ('first_name', 'second_name', 'last_name_father', 'last_name_mother', 'age', 'email')
