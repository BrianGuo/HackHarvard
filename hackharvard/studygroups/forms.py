from django import forms
from django.forms import ModelForm

from .models import Profile, Course, DateDuration, Group, DateDurationGroup


class ProfileForm(ModelForm):

    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.widgets.CheckboxSelectMultiple())

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'resume_or_linkedin', 'bio']


class DateDurationForm(forms.ModelForm):
    class Meta:
        model = DateDuration
        fields = ['date', 'time_start', 'time_end']


class DateDurationGroupForm(forms.ModelForm):
    class Meta:
        model = DateDurationGroup
        fields = ['date', 'time_start', 'time_end']


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['location', 'course', 'name']

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = self.profile.courses
