from django.urls import path
from . import views

app_name = "Loginify"

urlpatterns = [
    path("", views.hello_world, name="hello"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),

    # API CRUD endpoints
    path("api/users/", views.get_all_users, name="api_get_all_users"),
    path("api/users/<str:email>/", views.get_user_by_email, name="api_get_user_by_email"),
    path("api/users/<str:email>/update/", views.update_user, name="api_update_user"),
    path("api/users/<str:email>/delete/", views.delete_user, name="api_delete_user"),
]
