import json

from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from slacker import Slacker

from app_v2.decorators import guard
from app_v2.forms import LoginForm
from app_v2.models import SlackUser
from app_v2.utils import generate_guest_id


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


@csrf_exempt
def add_guest(request):
    try:
        payload = json.loads(request.body)
        user_type = payload.get("user_type")
        print(payload)
        if user_type == "guest":
            slack_id = generate_guest_id()
            total_guests = SlackUser.objects.filter(user_type="guest").count()
            firstname = f"Guest {total_guests + 1}"
            payload["firstname"] = firstname
            new_user = SlackUser(**payload, slack_id=slack_id)
            new_user.save()
            status = 200
            response = dict(
                firstname=new_user.firstname,
                email=new_user.email,
                slack_id=new_user.slack_id,
                id=new_user.id,
                lastname=new_user.lastname,
                is_active=new_user.is_active,
                photo=new_user.photo,
            )
        else:
            status = 400
            response = "Cannot create a non-GUEST user."
    except Exception as e:
        status = 400
        response = e.args[0]

    return JsonResponse(response, status=status, safe=False)


def signout(request):
    logout(request)
    return redirect("login")


def retrieve_user(request, firstname):
    users = SlackUser.objects.filter(firstname__icontains=firstname)
    response = list(users)
    return JsonResponse(response, status=status, safe=False)
