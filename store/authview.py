from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        Email = request.POST.get('email')
        raw_password = request.POST.get('password2')
        userEmail = User.objects.filter(email=Email)
        if form.is_valid():
            form.save()
            user = authenticate(email=Email, password=raw_password)
            messages.success(request, "Registered successfully!")
            return redirect('/login')
        else:
            print("in else")
            messages.error(request, "Email already in used")
            return redirect("/register")
    context = {'form': form}
    return render(request, "register.html", context)


def loginpage(request):
    if request.method == 'POST':
        Email = request.POST.get('email')
        passwd = request.POST.get('password')

        # if Email == 'admin@gmail.com':
        #     messages.error(request, "Access Denied")
        #     return redirect("/login")

        try:
            userEmail = User.objects.get(email=Email)
            if userEmail.is_staff:
                messages.error(request, "Access Denied")
                return redirect("/login")

        except User.DoesNotExist:
            userEmail = None

        if userEmail is not None:
            user = authenticate(request, username=userEmail.username, password=passwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid Email or Password")
                return redirect("/login")
        else:
            messages.error(request, "Invalid Email or Password")
            return redirect("/login")

    return render(request, "login.html")


def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successfully")
    return redirect("/login")




# def loginpage(request):
#     if request.method == 'POST':
#         Email = request.POST.get('email')
#         passwd = request.POST.get('password')
#
#         userEmail = User.objects.get(email=Email)
#         user = authenticate(request, username=userEmail.username, password=passwd)
#         print(user)
#         if user is not None:
#             login(request, user)
#             messages.success(request, "Login successfully")
#             return redirect("/")
#         else:
#             messages.error(request, "Invalid Email or Password")
#             return redirect("/login")
#     return render(request, "login.html")


# def register(request):
#     form = CustomUserForm()
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         # Email = request.POST.get('email')
#         # raw_password = request.POST.get('password2')
#
#         # userEmail = User.objects.get(email=Email)
#         # print(userEmail.username)
#         if form.is_valid():
#             form.save()
#             # user = authenticate(email=Email, password=raw_password)
#             # print(user)
#
#             messages.success(request, "Registered and logged in successfully!")
#             return redirect("/")
#         else:
#             messages.error(request, "Email already in used")
#             return redirect("/register")
#
#     context = {'form': form}
#     return render(request, "register.html", context)