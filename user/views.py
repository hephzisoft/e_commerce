from django.shortcuts import render,redirect

from user.forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

def signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'user/register.html', {'form': form})



def login(request):
    pass