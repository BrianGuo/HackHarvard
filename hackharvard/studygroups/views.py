from django.shortcuts import render


# Create your views here.
def home_page(request):
    return render(request, 'housingmanager/housing_group_home.html')
