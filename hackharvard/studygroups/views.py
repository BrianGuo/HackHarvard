from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib import messages
from .models import Profile, DateDuration, Group
from .forms import ProfileForm, DateDurationForm
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


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
        form = DateFormSet(request.POST, instance=profile)
        if form.is_valid():
            date_element = form.save(commit=False)
            for date in date_element:
                date.in_proposed_group = False
                date.save()
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
        for group in Group.objects.filter(meeting_time__date=time.date):
            timedelta = 0
            if (time.start < group.meeting_time.start):
                timedelta = time.end - group.meeting_time.start
            else:
                timedelta = group.meeting_time.end - time.start
            if timedelta.seconds >= 3600:
                results.push(group)
    return render(request, 'find_groups.html', {'groups': results})


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

    # groups = array(groups)
    return render(request, 'course_page.html', {'groups': groups, 'department': department, 'number': number, 'title': title})

def single_group(request, id):
    group = Group.objects.get(pk=id)
    return render(request, 'group.html', {'group': group})