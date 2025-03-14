from django import forms
from CarrierApp.models import Student


class Stud_profileForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['name', 'place', 'phone', 'age', 'Gender', 'email', 'qualification']
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"Full name"}),
            "place":forms.TextInput(attrs={"class":"form-control","placeholder":"Place"}),
            "phone":forms.NumberInput(attrs={"class":"form-control","placeholder":"Phone"}),
            "age":forms.NumberInput(attrs={"class":"form-control","placeholder":"Age"}),
            "Gender": forms.Select(attrs={"class": "form-select"}),  
            "email": forms.EmailInput(attrs={"class": "form-control","placeholder":"Email"}),  
            "qualification": forms.TextInput(attrs={"class": "form-control","placeholder":"Qualification"}),
        }
        




# forms.py


class CareerPreferenceForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    education = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialization = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    skills = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 
                                                         'placeholder': 'Enter comma-separated skills, e.g. Python, SQL, Communication'}))
    score = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}))