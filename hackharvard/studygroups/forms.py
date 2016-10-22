from django import forms
from django.forms import ModelForm

from .models import Profile, Course


class ProfileForm(ModelForm):

    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'resume_or_linkedin', 'bio']
