from django import forms
from CarrierApp.models import College,Course

class CollegeProfileForm(forms.ModelForm):
    class Meta:
        model=College
        fields=['name','place','Type','Description','cut_off_mark']
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control","placeholder":"College name"}),
            "place":forms.TextInput(attrs={"class":"form-control","placeholder":"Place"}),
            "Type":forms.Select(attrs={"class": "form-select"}),
            "Description":forms.Textarea(attrs={"class":"form-control","placeholder":"Description"}),
            "cut_off_mark": forms.NumberInput(attrs={"class": "form-control","placeholder":"Cutt-off Mark"}),  
            
        }
        


class AddCourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=['Courses']  
             
    