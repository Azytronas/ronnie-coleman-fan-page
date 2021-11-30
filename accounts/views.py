from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import LoginForm, RegisterForm
from django import forms

User = get_user_model()


def signup_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        user = User.objects.create_user(username, "", password)
        print(user.password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            request.session['register_error'] = 1  # 1 == True
    return render(request, "forms.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        if user is None:
            request.session['invalid_user'] = 1
    return render(request, "forms.html", {"form": form})


def logout_view(request):
    logout(request)
    print("logged out")
    return redirect("/")
