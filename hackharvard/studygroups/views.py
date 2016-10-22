from django.shortcuts import render
from .models import FullProfile, Profile
from .forms import ProfileForm

# Create your views here.
def new_profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        form.save(commit=False)
        user = get_user_model().objects.get(id=int(request.user.id))
        form.user = user
        form.save()
        return redirect(reverse('new_times'))
    return render(request, 'new_profile.html', {'form': form})

def new_times(request):
    form = FreeTimeForm()
    if request.method == 'POST':
        form = FreeTimeForm(request.POST)
        form.save()
        profile = Profile.objects.get(user=get_user_model().objects.get(id=request.user.id))
        fullprof = FullProfile(profile=profile, free_time=form)
        return redirect(reverse('groups', kwargs={'profile': form}))
    return render(request, 'group_page.html', {'form': form})