from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

# Test view 
def hello_world(request):
    return HttpResponse("Hello, world!")

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login successful")
        return HttpResponse("Invalid credentials", status=401)

    # Basic HTML form
    return HttpResponse(
        "<form method='post'>"
        "Username: <input name='username'><br>"
        "Password: <input type='password' name='password'><br>"
        "<input type='submit' value='Login'>"
        "</form>"
    )
