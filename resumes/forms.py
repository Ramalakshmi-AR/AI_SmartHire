from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['name', 'email', 'experience', 'uploaded_file']

    def clean_uploaded_file(self):
        file = self.cleaned_data.get('uploaded_file')
        if file:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
        return file
