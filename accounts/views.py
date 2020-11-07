from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            success_message = 'Successfully created new account!'
            context = {'form': form, 'success_message': success_message}
            return render(request, "accounts/signup.html", context)
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            success_message = "Sucessfully logged in!"
            context = {'form': form, 'success_message': success_message}
            return render(request, "accounts/login.html", context)
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
