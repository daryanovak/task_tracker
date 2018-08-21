from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm



def index(request):
    return render(request, 'accounts/signup.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/login')

    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})

