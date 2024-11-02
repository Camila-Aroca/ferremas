from typing import Any
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from .models import Cliente, TipoTarjeta, Tarjeta


class RegistroUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nombre = forms.CharField(required=True)
    apellido_paterno = forms.CharField(required=True)
    apellido_materno = forms.CharField(required=True)
    telefono = forms.CharField(required=True, max_length=12, widget=forms.TextInput(attrs={'placeholder': 'Número de teléfono (Ej: 123456789)'}))
    aceptar_terminos = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = ("email", "nombre", "apellido_paterno", "apellido_materno", "telefono", "password1", "password2")

   

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'genero', 'fecha_nacimiento', 'clave', 'correo', 'es_miembro']

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}),
            'clave': forms.PasswordInput(),
        }

class TipoTarjetaForm(forms.ModelForm):
    class Meta:
        model = TipoTarjeta
        fields = ['id_tipo', 'descripcion']


class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['numero_tarjeta', 'cvv', 'tipo', 'cliente']
        widgets = {
            'numero_tarjeta': forms.TextInput(attrs={'placeholder': 'Número de Tarjeta'}),
            'cvv': forms.TextInput(attrs={'placeholder': 'CVV'}),
        }
