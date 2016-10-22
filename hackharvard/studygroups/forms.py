from django import forms
from django.forms import ModelForm

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'courses', 'free_time', 'resume_or_linkedin', 'bio'] 