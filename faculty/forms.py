from django import forms
from CarrierApp.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies', 'image', 'repository_link', 'demo_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'technologies': forms.TextInput(attrs={'placeholder': 'Python, Django, JavaScript, etc.'}),
        }