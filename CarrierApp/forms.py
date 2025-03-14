from django import forms
from CarrierApp.models import Login

class Registration(forms.ModelForm):
    class Meta:
        model=Login
        fields=['username','name','is_student','email','password','is_faculty']

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()        

