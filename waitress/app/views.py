from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from waitress.app.forms import LoginForm
from app.models import MealService
from app.utils import serialize_meal_service

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
        if request.GET.get('date'):
            report_date = request.GET.get('date')
            meal_service = MealService.objects.filter(date=report_date).all()
            return JsonResponse({
                'status': 'success',
                'data': serialize_meal_service(meal_service)
            })
        return render(request, "daily_report.html")
