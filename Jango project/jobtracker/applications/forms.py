from django import forms
from .models import JobApplication, TrackedCompany


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['company', 'role', 'status', 'deadline']


class TrackedCompanyForm(forms.ModelForm):
    class Meta:
        model = TrackedCompany
        fields = ['name', 'career_url']


#user sign up

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
