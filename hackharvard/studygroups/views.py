from django.shortcuts import render, render_to_response
from django.db import IntegrityError
from django.contrib import messages
from .models import FullProfile, Profile
from .forms import ProfileForm, FreeTimeForm
from django.contrib.auth import get_user_model

# Create your views here.


def new_profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        print(request.POST)
        if form.is_valid():
            try:
                form = ProfileForm(request.POST)
                profile = form.save(commit=False)
                user = get_user_model().objects.get(id=int(request.user.id))
                profile.user = user
                profile.save()
                return render(request, 'new_times.html', {'form': form})
            except IntegrityError:
                form = ProfileForm()
                messages.error(request, "Looks like you're already registered")
                return render(request, 'new_profile.html', {'form': form})
        else:
            print("form not valid")
    return render(request, 'new_profile.html', {'form': form})


def new_times(request):
    form = FreeTimeForm()
    if request.method == 'POST':
        form = FreeTimeForm(request.POST)
        form.save()
        profile = Profile.objects.get(user=get_user_model().objects.get(id=request.user.id))
        fullprof = FullProfile(profile=profile, free_time=form)
        return redirect(reverse('groups', kwargs={'profile': form}))
    return render(request, 'new_times.html', {'form': form})


def view_profile(request):
    profile = Profile.objects.get(user=get_user_model().objects.get(id=request.user.id))
    return render(request, 'profile.html', {'profile': profile})

