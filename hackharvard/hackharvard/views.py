import datetime

from django.shortcuts import render
from django.utils.timezone import now
from django.dispatch import receiver
from django.conf import settings


def home(request):
    today = datetime.date.today()
    return render(request, 'index.html',
                  {'today': today, 'now': now()})
