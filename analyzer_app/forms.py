from django import forms
from .models import User,StockData
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm 
 
 
class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("email",)


class StockDataForm(ModelForm):
    class Meta:
        model = StockData
        fields = [
            "date",
            "trade_code",
            "high",
            "low",
            "open",
            "close",
            "volume",
        ]



