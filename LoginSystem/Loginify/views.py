from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json

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

def get_all_users(request):
    """Return JSON list of all users."""
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    users = list(UserDetails.objects.values("username", "email"))
    return JsonResponse(users, safe=False)

def get_user_by_email(request, email):
    """Return JSON details for a single user found by email."""
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    user = get_object_or_404(UserDetails, email=email)
    return JsonResponse({"username": user.username, "email": user.email})

@csrf_exempt
def update_user(request, email):
    """Update user fields (username, password, email) for the user identified by email.
    Accepts JSON body (for PUT) or form data (for POST) for easy Postman testing.
    """
    if request.method not in ("PUT", "POST"):
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = get_object_or_404(UserDetails, email=email)

    if request.method == "PUT":
        try:
            data = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        data = request.POST

    username = data.get("username")
    new_email = data.get("email")
    password = data.get("password")

    if username:
        user.username = username
    if new_email:
        # check unique
        if UserDetails.objects.exclude(pk=user.pk).filter(email=new_email).exists():
            return JsonResponse({"error": "Email already in use"}, status=400)
        user.email = new_email
    if password:
        user.password = password

    user.save()
    return JsonResponse({"username": user.username, "email": user.email})

@csrf_exempt
def delete_user(request, email):
    """Delete a user identified by email. Accepts DELETE or POST for easy testing."""
    if request.method not in ("DELETE", "POST"):
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = get_object_or_404(UserDetails, email=email)
    user.delete()
    return JsonResponse({"deleted": True})
