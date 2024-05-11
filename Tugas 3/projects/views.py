from django.shortcuts import render

from account.models import Account


# Create your views here.

def home_screen_view(request):
    context = {}

    account= Account.objects.all()
    context['account'] = account

    return render(request, "projects/home.html", context)