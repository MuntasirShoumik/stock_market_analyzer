from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
 
 
 
class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("email",)