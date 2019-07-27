from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from slacker import Slacker

from app_v2.decorators import guard
from app_v2.forms import LoginForm
from app_v2.models import SlackUser


slack = Slacker(settings.SLACK_API_TOKEN)


# Create your views here.
def login_handler(request):
    context = {"login_form": LoginForm}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        form = LoginForm(request.POST)
        is_form_valid = form.is_valid()
        error_message = "Error logging in. Kindly check your username or password"
        request.session["error_message"] = error_message

        if not is_form_valid:
            return redirect("login")

        user = authenticate(username=username, password=password)
        if not user:
            return redirect("login")

        login(request, user)
        return redirect("dashboard")

    return render(request, "index.html", context)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "dashboard.html")


# @guard
def fetch_users(request):
    all_users = list(SlackUser.objects.values())
    return JsonResponse(all_users, status=200, safe=False)


# @guard
def refresh_slack_users(request):
    # all_users = SlackUser.objects.all()
    return JsonResponse({"data": "users"}, status=200)


def signout(request):
    logout(request)
    return redirect("login")
