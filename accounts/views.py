from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":

        # Get form values
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # check if passwords match
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is taken.")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "That email belongs to an existing user.")
                return redirect("register")
            else:
                # looks good
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                # login after register
                # auth.login(request, user)
                # messages.success(f"User created successfully.")
                # return redirect("/")
                messages.success(
                    request,
                    f"Successfully signed up as {user.username}. Please log in.",
                )
                return redirect("login")

        else:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        return redirect("register")
    else:
        return render(request, "accounts/register.html")


def login(request):
    if request.method == "POST":
        # Login user
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect("login")
    else:
        return render(request, "accounts/login.html")


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.info(request, "You are now logged out.")
        return redirect("index")


def dashboard(request):
    return render(request, "accounts/dashboard.html")