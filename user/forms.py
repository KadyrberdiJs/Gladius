from django import forms
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm, UserChangeForm

from user.models import User

class UserLoginForm(AuthenticationForm):
  username = forms.CharField()
  password = forms.CharField()

  class Meta:
    model = User
    fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
  username = forms.CharField()
  email = forms.EmailField()
  password1 = forms.CharField()
  password2 = forms.CharField()

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(UserChangeForm):
  class Meta:
    model = User
    fields = ['image','username', 'email', ]
    
  image = forms.ImageField(required=False)
  username = forms.CharField()
  email = forms.EmailField()
