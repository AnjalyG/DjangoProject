from django.urls import path
from . import views

app_name = "Loginify"

urlpatterns = [
    path("", views.hello_world, name="hello"),
    path("login/", views.login_view, name="login"),
]
