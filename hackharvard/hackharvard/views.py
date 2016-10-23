import datetime

from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.dispatch import receiver
from django.conf import settings

from studygroups.forms import ProfileForm


def home(request):
    return render(request, 'homepage.html')

