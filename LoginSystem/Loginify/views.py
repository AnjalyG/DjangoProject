from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import UserDetails

# Test view 
def hello_world(request):
    return HttpResponse("Hello, world!")

def signup_view(request):
    """Handle user registration."""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # basic validation
        if not username or not email or not password:
            return render(request, "Loginify/signup.html", {"error": "All fields are required."})

        # ensure email is unique
        if UserDetails.objects.filter(email=email).exists():
            return render(request, "Loginify/signup.html", {"error": "Email already registered."})

        # create user
        user = UserDetails.objects.create(username=username, email=email, password=password)

        # render a confirmation page that redirects to login
        return render(request, "Loginify/signup_confirmation.html", {"username": user.username, "email": user.email})

    return render(request, "Loginify/signup.html")

def login_view(request):
    """Handle login using email and password against UserDetails model."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        try:
            user = UserDetails.objects.get(email=email)
        except UserDetails.DoesNotExist:
            return render(request, "Loginify/login.html", {"error": "Invalid credentials."})

        if user.password == password:
            # success
            return render(request, "Loginify/login_success.html", {"username": user.username, "email": user.email})
        # Login error
        return render(request, "Loginify/login.html", {"error": "Invalid credentials."})

    return render(request, "Loginify/login.html")
