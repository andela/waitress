from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from waitress.app.forms import LoginForm


schema_view = get_schema_view(
    openapi.Info(
        title="Andela Waitress App",
        default_version="v1",
        description="Swagger Documentation for the waitress app.",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


def login_handler(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    context = dict(login_form=LoginForm)
    if request.method == "POST":
        error_message = "Username or Password incorrect."
        username = request.POST.get("username")
        password = request.POST.get("password")
        form = LoginForm(request.POST)

        if not form.is_valid():
            messages.add_message(request, messages.ERROR, error_message)
            return redirect("login")

        user = authenticate(username=username, password=password)
        if not user:
            messages.add_message(request, messages.ERROR, error_message)
            return redirect("login")

        login(request, user)
        return redirect("dashboard")

    return render(request, "login.html", context)


def dashboard(request):
    return render(request, "dashboard.html")
