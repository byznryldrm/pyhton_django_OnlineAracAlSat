from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from car.models import Car
from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets= {
            'username' : TextInput (attrs = {'class': 'input', 'placeholder': 'Kullanıcı Adı'}),
            'email': EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'Adı'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'Soyadı'}),
        }

CITY = [
    ('Istanbul','Istanbul'),
    ('Ankara','Ankara'),
    ('Izmir','Izmir'),
    ('Karabük','Karabük'),
]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'country','image')
        widgets= {
            'phone' : TextInput (attrs = {'class': 'input', 'placeholder': 'Telefon'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'Adres'}),
            'city': Select(attrs={'class': 'input', 'placeholder': 'Şehir'} , choices=CITY),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'Ülke'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'Fotoğraf'}),
        }

class CarAddForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['title', 'description', 'price', 'image', 'detail', 'status', 'slug']
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'price': TextInput(attrs={'class': 'input', 'placeholder': 'price'}),
            'status': Select(attrs={'class': 'input', 'placeholder': 'status'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'detail': CKEditorWidget(),
        }