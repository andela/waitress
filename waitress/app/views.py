from datetime import date, datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, Count, Value, When
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as status_code

from app.models import MealService
from app.utils import serialize_meal_service
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


class LoginHandler(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")

        context = dict(login_form=LoginForm)
        return render(request, "login.html", context)

    def post(self, request):
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


class Dashboard(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        return render(request, "dashboard.html")


class LogoutHandler(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        logout(request)
        return redirect("login")


class DailyReportHandler(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        if request.GET.get("date"):
            report_date = request.GET.get("date")
            report_type = request.GET.get("reportType")

            if report_type == "lunch":
                queryset = MealService.objects.filter(date=report_date, lunch=True)
            elif report_type == "breakfast":
                queryset = MealService.objects.filter(date=report_date, breakfast=True)
            else:
                queryset = MealService.objects.filter(date=report_date)

            meal_service = queryset.all()
            meal_count = queryset.aggregate(
                breakfast_count=Count(Case(When(breakfast=True, then=Value(1)))),
                lunch_count=Count(Case(When(lunch=True, then=Value(1)))),
            )
            response = {
                "status": "success",
                "data": serialize_meal_service(meal_service),
                **meal_count,
            }
            return JsonResponse(response)
        return render(request, "daily_report.html")


class WeeklyReportHandler(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        from_date = request.GET.get("from")
        to_date = request.GET.get("to")
        return render(request, "weekly_report.html")


class ChangePasswordHandler(LoginRequiredMixin, View):
    login_url = "/"

    def get(self, request):
        return render(request, "change_password.html")

    def patch(self, request):
        payload = json.loads(request.body)
        passwordText = payload.get("passwordText")
        verifyPasswordText = payload.get("verifyPasswordText")

        if passwordText != verifyPasswordText:
            return JsonResponse({}, status=400)

        request.user.set_password(passwordText)
        request.user.save()

        return JsonResponse({"status": "success"}, status=200)
