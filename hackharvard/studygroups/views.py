from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib import messages
from .models import Profile, DateDuration
from .forms import ProfileForm, DateDurationForm
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.db.models import Q


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
                return redirect(reverse('studygroups:new_times'))
            except IntegrityError:
                form = ProfileForm()
                messages.error(request, "Looks like you're already registered")
                return render(request, 'new_profile.html', {'form': form})
        else:
            print("form not valid")
    return render(request, 'new_profile.html', {'form': form})


def new_times(request):
    DateFormSet = inlineformset_factory(
        Profile, DateDuration, fields=('date', 'time_start', 'time_end'), form=DateDurationForm)
    profile = Profile.objects.get(user=get_user_model().objects.get(id=request.user.id))
    formset = DateFormSet(instance=profile)
    if request.method == 'POST':
        form = DateFormSet(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('studygroups:groups', kwargs={'profile': form}))
        else:
            print(form.errors)
    return render(request, 'new_times.html', {'formset': formset})

def groups(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    queryset = profile.dateduration_set.all()



def view_profile(request):
    profile = Profile.objects.get(user=get_user_model().objects.get(id=request.user.id))
    return render(request, 'profile.html', {'profile': profile})
