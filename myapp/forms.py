from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import Customer

class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
  email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
    labels = {'username': 'Full Name'}
    widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}
    
class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ChangePasswordForm(PasswordChangeForm):
  old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
  new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
  new_password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))
  class Meta:
    model = User
    fields = ['old_password', 'new_password1', 'new_password2']
    
class CustomerProfile(forms.ModelForm):
  class Meta:
   model = Customer
   fields = ['name', 'locality', 'city', 'state', 'zipcode']
   widgets = {
     'name': forms.TextInput(attrs={'class':'form-control'}),
     'locality': forms.TextInput(attrs={'class':'form-control'}),
     'city': forms.TextInput(attrs={'class':'form-control'}),
     'state': forms.Select(attrs={'class':'form-control'}),
     'zipcode': forms.NumberInput(attrs={'class':'form-control'}),
   }