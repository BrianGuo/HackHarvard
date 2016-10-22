import datetime

from django.shortcuts import render
from django.utils.timezone import now
from django.dispatch import receiver
from django.conf import settings

from studygroups.forms import ProfileForm


def home(request):
    return render(request, 'homepage.html')


def new_profile(request):
    form = ProfileForm(request.POST)
    return render(request, 'new_profile.html', {'form': form})
