import datetime

from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.dispatch import receiver
from django.conf import settings

from studygroups.forms import ProfileForm


def home(request):
    return render(request, 'homepage.html')


def new_profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        form.save()
        return redirect(reverse('new_times', kwargs={'profile': form}))
    return render(request, 'new_profile.html', {'form': form})

def new_time(request):
    form = FullProfileForm()
    if request.method == 'POST':
        form = FullProfileForm(request.POST)
        form.save()
        return redirect(reverse('groups', kwargs={'profile': form}))
    return render(request, 'group_page.html', {'form': form})
