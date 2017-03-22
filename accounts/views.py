from django.shortcuts import render, redirect
# Create your views here.

from .forms import UserLoginForm, UserRegisterForm

from django.contrib.auth import authenticate, login, logout


def login_view(request):
    print request.user.is_authenticated()
    
    next = request.GET.get("next")
    
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        print request.user.is_authenticated
        
        if next:
            return redirect(next)
        return redirect("/blog/list")
        
    return render(request, "form.html", {"form": form})

def logout_view(request):
    logout(request)
    return render(request, "form.html", {})

def register_view(request):
    next = request.GET.get("next")
    
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        
        if next:
            return redirect(next)
        return redirect("/blog/list")
    context = {
        "form": form
    }
    return render(request, "form.html", context)

