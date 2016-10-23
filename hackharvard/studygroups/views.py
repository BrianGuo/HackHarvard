from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib import messages
from .models import Profile, DateDuration, Group
from .forms import ProfileForm, DateDurationForm, GroupForm, DateDurationGroupForm
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from datetime import datetime, date
# Create your views here.


def new_profile(request):
    try:
        profile = request.user.profile
        return redirect(reverse('studygroups:new_times'))
    except ObjectDoesNotExist:
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
        print(request.POST)
        form = DateFormSet(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('studygroups:groups'))
        else:
            print(form.errors)
    return render(request, 'new_times.html', {'formset': formset})


def groups(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    queryset = profile.dateduration_set.all()
    results = []
    for time in queryset:
        for group in Group.objects.filter(datedurationgroup__date=time.date):
            timedelta = 0
            if (time.time_start < group.datedurationgroup.time_start):
                timedelta = datetime.combine(
                    date.min, time.time_end) - datetime.combine(date.min, group.datedurationgroup.time_start)
            else:
                timedelta = datetime.combine(
                    date.min, group.datedurationgroup.time_end) - datetime.combine(date.min, time.time_start)
            if timedelta.seconds >= 3600:
                results.append(group)
    return render(request, 'find_groups.html', {'groups': results})


def view_profile(request):
    profile = Profile.objects.get(user=get_user_model().objects.get(id=request.user.id))
    return render(request, 'profile.html', {'profile': profile})


def create_group(request):
    groupform = GroupForm(profile=request.user.profile)
    meeting_time_form = DateDurationGroupForm()
    if request.method == 'POST':
        subdict = {'date': request.POST['date'], 'time_start': request.POST[
            'time_start'], 'time_end': request.POST['time_end']}
        meeting_time_form = DateDurationGroupForm(subdict)
        if meeting_time_form.is_valid():
            meeting_time = meeting_time_form.save(commit=False)
            rest_dict = {'location': request.POST['location'], 'course': request.POST['course']}
            groupform = GroupForm(rest_dict, profile=request.user.profile)
            if groupform.is_valid():
                group = groupform.save(commit=False)
                profile = Profile.objects.get(user=request.user)
                group.save()
                group.members.add(profile)
                meeting_time.group = group
                meeting_time.save()
                return redirect(reverse('studygroups:groups'))
        return redirect(reverse('studygroups:new_group'))
    return render(request, 'group_create.html', {'groupform': groupform, 'meetingform': meeting_time_form})

def accept_invite(request, ):

