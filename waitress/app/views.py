from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views import View
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from django.http import JsonResponse

from app.models import SlackUser
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
        users_query_set = SlackUser.objects.order_by("id")
        users_list = users_query_set.all()
        active_users_count = users_query_set.filter(is_active=True).count()
        inactive_users_count = users_query_set.filter(is_active=False).count()
        paginator = Paginator(users_list, 25)  # Show 25 users per page
        paginated_users = paginator.get_page(1)
        end_index = paginated_users.end_index()

        context = dict(
            users=paginated_users,
            total_users=len(users_list),
            total_active_users=active_users_count,
            total_inactive_users=inactive_users_count,
            pages=range(end_index),
        )
        return render(request, "dashboard.html", context)


# class UserHandler(LoginRequiredMixin, View):
class UserHandler(View):
    login_url = "/"
    limit = 25

    def get(self, request):
        users_query_set = SlackUser.objects.order_by("id")
        users_list = users_query_set.all()
        active_users_count = users_query_set.filter(is_active=True).count()
        inactive_users_count = users_query_set.filter(is_active=False).count()
        paginator = Paginator(users_list, self.limit)  # Show 25 users per page
        paginated_users = paginator.get_page(1)
        end_index = paginated_users.end_index()
        return JsonResponse([], safe=False)
