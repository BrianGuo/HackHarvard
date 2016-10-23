from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib import messages
from .models import Profile, DateDuration, Group, Course
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
                    print(request.body)
                    for course_pk in dict(request.POST)['courses']:
                        course = Course.objects.get(id=course_pk)
                        print(course)
                        profile.courses.add(course)
                        profile.save()
                    print(profile.courses.all())
                    return redirect(reverse('studygroups:new_times'))
                except IntegrityError:
                    form = ProfileForm()
                    messages.error(request, "Looks like you're already registered")
                    return render(request, 'new_profile.html', {'form': form})
            else:
                print("form not valid")
    return render(request, 'new_profile.html', {'form': form})


def new_times(request):
    if (request.user.profile.dateduration_set.first() is not None):
        return redirect(reverse('studygroups:groups'))
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
    return render(request, 'find_groups.html', {'groups': results, 'profile': profile})


def view_profile(request):
    profile = Profile.objects.get(user=get_user_model().objects.get(id=request.user.id))
    return render(request, 'profile.html', {'profile': profile})

def course(request, department, number):
    groups = Group.objects.filter(course__department=department).filter(course__number=number)

    if (groups.count() != 0):
        department = groups.get(pk=1).course.department
        number = groups.get(pk=1).course.number
        title = groups.get(pk=1).course.title
    else:
        department = "No"
        number = "Groups"
        title = "Yet"

    return render(request, 'course_page.html', {'groups': groups, 'department': department, 'number': number, 'title': title})

def single_group(request, pk):
    group = Group.objects.get(id=pk)
    profile = Profile.objects.get(user=request.user)
    if(profile not in group.members.all()):
        messages.error(request, "You're not a member of this group!")
        return redirect(reverse("studygroups:groups"))
    return render(request, 'group.html', {'group': group})

def create_group(request):
    groupform = GroupForm(profile=request.user.profile)
    meeting_time_form = DateDurationGroupForm()
    if request.method == 'POST':
        subdict = {'date': request.POST['date'], 'time_start': request.POST[
            'time_start'], 'time_end': request.POST['time_end']}
        meeting_time_form = DateDurationGroupForm(subdict)
        if meeting_time_form.is_valid():
            meeting_time = meeting_time_form.save(commit=False)
            rest_dict = {'location': request.POST['location'], 'course': request.POST['course'], 'name': request.POST['name']}
            groupform = GroupForm(rest_dict, profile=request.user.profile)
            if groupform.is_valid():
                group = groupform.save(commit=False)
                profile = Profile.objects.get(user=request.user)
                group.save()
                group.members.add(profile)
                meeting_time.group = group
                meeting_time.save()
                return redirect(reverse('studygroups:groups'))
            else:
                print(groupform.errors)
        else:
            print(meeting_time_form.errors)
        return redirect(reverse('studygroups:new_group'))
    return render(request, 'group_create.html', {'groupform': groupform, 'meetingform': meeting_time_form})

def request_group(request, pk):
    profile = Profile.objects.get(user=request.user)
    group = Group.objects.get(id=pk)
    if request.method == 'POST':
        if profile in group.invited.all():
            messages.error("You have already requested to join this group")
            return redirect(reverse('studygroups:groups'))
        else:
            group.invited.add(profile)
    return redirect(reverse('studygroups:groups'))

def respond_invite(request, group_pk):
    if request.method == 'POST':
        for pk, decision in request.POST.items():
            if decision == "Accept":
                user = get_user_model().objects.get(id=pk)
                profile = Profile.objects.get(user=user)
                group = Group.objects.get(id=group_pk)
                group.members.add(profile)
            group.invited.remove(profile)
    return redirect(reverse('studygroups:single_group', kwargs={'pk': group_pk}))