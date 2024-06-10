from django import forms
from django.contrib.auth.models import User
from .models import Student

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class StudentForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Student
        fields = ['full_name', 'birth_date', 'email', 'group']
