from django.shortcuts import render
from django.utils.timezone import now
from django.dispatch import receiver
from django.conf import settings


def home(request):
    return render(request, 'homepage.html')
