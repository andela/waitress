import json
from datetime import date

import pytz
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status as status_code
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.decorators import guard
from app.models import MealService, MealSession, SlackUser, Pantry, Passphrase
from app.serializers import (
    FilterSerializer,
    ReportSerializer,
    SecureUserSerializer,
    UserSerializer,
)
from app.utils import Time, UserRepository


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    queryset = SlackUser.objects.all()

    @swagger_auto_schema(query_serializer=FilterSerializer)
    def list(self, request):
        """
        A method that gets the list of users.
        ---
        parameters:
            - name: filter
              description: query based on firstname
              required: false
              type: string
              paramType: query
        """
        filter = request.GET.get("filter")
        queryset = self.queryset

        if request.GET.get("filter"):
            queryset = queryset.filter(firstname__startswith=filter).order_by(
                "firstname"
            )
        else:
            queryset = queryset.all().order_by("id")
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data, status_code.HTTP_200_OK)

    @swagger_auto_schema()
    @action(methods=["post"], url_path="retrieve-secure", detail=True)
    def retrieve_securely(self, request, pk):
        """
        A method that gets the details of a user.
        ---
        parameters:
            - name: pk
              description: unique id of the user
              required: true
              type: string
              paramType: path
            - name: passphrase
              description: passphrase to allow authentication
              required: true
              type: string
              paramType: form
        """
        queryset = get_object_or_404(self.queryset, pk=pk)
        serializer = SecureUserSerializer(queryset)
        return Response(serializer.data, status_code.HTTP_200_OK)

    @swagger_auto_schema()
    @action(methods=["put"], detail=True, url_path="toggle-user-active")
    def toggle_user_active_status(self, request, pk):
        """
        A method that is used to toggle a user's active status
        ---
        parameters:
            - pk: user_id
              description: unique id of the user
              required: true
              type: string
              paramType: path
        """
        user = get_object_or_404(self.queryset, pk=pk)
        user.is_active = not user.is_active
        serializer = SecureUserSerializer(user)
        user.save()
        return Response(serializer.data, status_code.HTTP_200_OK)

    @action(methods=["get"], url_path="update-users", detail=False)
    def update_users(self, request):
        """
        A method that updates the list of users.
        """
        status = UserRepository.update()
        content = {"status": status}

        return Response(content, status=status_code.HTTP_200_OK)

    @action(methods=["get"], url_path="regularize-guest-names", detail=False)
    def regularize_guests(self, request):
        """
        A method that regularizes the names of guests.
        """
        status = UserRepository.regularize_guests()
        content = {"status": status}

        return Response(content, status=status_code.HTTP_200_OK if status else 500)

    @action(methods=["get"], url_path="remove-old-friends", detail=False)
    def trim_users(self, request):
        """
        A method that trims the list of users.
        """
        status = UserRepository.update(trim=True)
        content = {"status": status}

        return Response(content, status=status_code.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "firstname": openapi.Schema(
                    type=openapi.TYPE_STRING, description="firstname"
                ),
                "lastname": openapi.Schema(
                    type=openapi.TYPE_STRING, description="lastname"
                ),
                "utype": openapi.Schema(
                    type=openapi.TYPE_STRING, description="user type", default="guest"
                ),
                "passphrase": openapi.Schema(
                    type=openapi.TYPE_STRING, description="Passphrase"
                ),
            },
        )
    )
    @guard
    @action(methods=["post"], url_path="add", detail=False)
    def add_user(self, request):
        """
        A method that adds a guest to the list of users.
        ---
        parameters:
            - name: firstname
              description: firstname of the user
              required: true
              type: string
              paramType: form
            - name: lastname
              description: lastname of the user
              required: true
              type: string
              paramType: form
            - name: utype
              description: type of the user (security|cleaner|chef|guest)
              required: true
              type: string
              paramType: form
            - name: passphrase
              description: passphrase to allow authentication
              required: true
              type: string
              paramType: form
        """
        user_data = request.POST.dict() or request.data
        status, user_id = UserRepository.add(**user_data)
        content = {"status": status}
        if user_id:
            content["user_id"] = user_id
            return Response(content, status=status_code.HTTP_200_OK)
        return Response(content, status=304)

    @action(methods=["post"], url_path="nfctap", detail=False)
    def nfctap(self, request):
        """
        A method that taps a user via an NFC card.
        ---
        parameters:
            - name: slackUserId
              description: slack ID
              required: true
              type: string
              paramType: form
        """
        slack_id = request.POST.get("slackUserId")

        if not slack_id:
            content = {"status": "You're  unauthorized to make this request"}
            return Response(content, status=status_code.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(self.queryset, slack_id=slack_id)
        meal_in_progress = MealSession.in_progress()
        content = {"firstname": user.firstname, "lastname": user.lastname}

        if not user.is_active:
            content["status"] = "User has been deactivated. Contact the Ops team."
            return Response(content, status=status_code.HTTP_400_BAD_REQUEST)

        if not meal_in_progress:
            content["status"] = "There is no meal in progress"
            return Response(content, status=status_code.HTTP_406_NOT_ACCEPTABLE)

        before_midday = Time.is_before_midday()

        if user.is_tapped():
            meal_type = "breakfast" if before_midday else "lunch"
            content["status"] = f"User has tapped in for {meal_type}"
            return Response(content, status=status_code.HTTP_400_BAD_REQUEST)

        date_today = meal_in_progress[0].date
        mealservice = MealService.objects.filter(user=user, date=date_today)

        mealservice = mealservice[0] if mealservice.count() else MealService()
        mealservice = mealservice.set_meal(before_midday)
        mealservice = mealservice.set_user_and_date(user, date_today)
        mealservice.save()

        content["status"] = "Tap was successful"

        return Response(content, status=status_code.HTTP_200_OK)

    @guard
    @swagger_auto_schema()
    @action(methods=["post"], url_path="untap", detail=True)
    def untap(self, request, pk):
        """
        A method that untaps a user.
        ---
        parameters:
            - name: pk
              description: unique id of the user
              required: true
              type: string
              paramType: path
            - name: passphrase
              description: passphrase to allow authentication
              required: true
              type: string
              paramType: form
        """
        before_midday = Time.is_before_midday()
        content = {}
        meal_in_progress = MealSession.in_progress()
        timenow = timezone.now()
        user = get_object_or_404(self.queryset, pk=pk)
        mealservice = MealService.objects.get(user=user, date=meal_in_progress[0].date)
        status = status_code.HTTP_200_OK

        if not meal_in_progress:
            content["status"] = "There is no meal in progress"
        else:
            mealservice = mealservice.set_meal(before_midday, reverse=True)
            if not mealservice.untapped:
                untapped = []
            else:
                untapped = json.loads(mealservice.untapped)
            log = {"date_untapped": str(timenow)}
            untapped.append(log)
            mealservice.untapped = untapped
            mealservice.date_modified = timenow
            mealservice.save()
            content["status"] = "Untap was successful"

        return Response(content, status=status)


class PantryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for accessing Pantry details
    """

    queryset = Pantry.objects.all()

    @action(methods=["post"], url_path="tap", detail=False)
    def pantrytap(self, request):
        """
        A method that taps a user via an NFC card for the pantry service
        ---
        parameters:
            - name: slackUserId
              description: slack ID
              required: true
              type: string
              paramType: form
        """
        slack_id = request.POST.get("slackUserId")

        if not slack_id:
            content = {"message": "You're  unauthorized to make this request"}
            return Response(content, status=status_code.HTTP_401_UNAUTHORIZED)

        user = SlackUser.objects.filter(slack_id=slack_id).first()

        if not user:
            content = {"message": "The user doesnt exist on waitress"}
            return Response(content, status=status_code.HTTP_404_NOT_FOUND)
        user_tapped = Pantry.is_tapped(user.id)
        content = {"firstname": user.firstname, "lastname": user.lastname}

        if not user.is_active:
            content[
                "message"
            ] = f"{user.firstname} has been deactivated. Contact the Ops team."
            return Response(content, status=status_code.HTTP_400_BAD_REQUEST)

        if user_tapped:
            content["message"] = f"{user.firstname} has tapped already."
            return Response(content, status=status_code.HTTP_406_NOT_ACCEPTABLE)

        content["message"] = f"{user.firstname} has successfully tapped."
        user_pantry_session = Pantry(user=user)
        user_pantry_session.save()

        return Response(content, status=status_code.HTTP_200_OK)

    @action(methods=["post"], url_path="auth", detail=False)
    def auth(self, request):
        passphrase = request.POST.get("passphrase", "")

        if not passphrase:
            content = {"status": "failed", "message": "Passphrase not supplied"}
            return Response(content, status=status_code.HTTP_400_BAD_REQUEST)

        exists = Passphrase.exists(passphrase)

        if not exists.status:
            content = {
                "status": "failed",
                "message": "Invalid Passphrase. Reach out to Ops!",
            }
            return Response(content, status=status_code.HTTP_401_UNAUTHORIZED)

        content = {"status": "success", "message": "Successfully authenticated."}
        return Response(content, status=status_code.HTTP_200_OK)

    @action(methods=["get"], url_path="report", detail=False)
    def report(self, request):
        reportDate = request.GET.get("date", date.today())

        queryset = self.queryset.filter(date=reportDate).order_by("date")

        content = {
            "status": "success",
            "data": {"date": reportDate, "count": queryset.count()},
        }

        return Response(content, status=status_code.HTTP_200_OK)


class MealSessionViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving meal session.
    """

    queryset = MealSession.objects.all()

    def list(self, request):
        """
        A method that tells if time is before mid-day or not.
        """
        before_midday = Time.is_before_midday()
        content = {"before_midday": before_midday}

        return Response(content, status=status_code.HTTP_200_OK)

    @guard
    @swagger_auto_schema()
    @action(methods=["post"], url_path="start", detail=False)
    def start(self, request):
        """
        A method that starts meal session.
        ---
        parameters:
            - name: before_midday
              description: is the time before or after 12 noon?
              required: true
              type: boolean
              paramType: form
            - name: passphrase
              description: passphrase to allow authentication
              required: true
              type: string
              paramType: form
        """

        # https://buildmedia.readthedocs.org/media/pdf/django-rest-swagger/stable-0.3.x/django-rest-swagger.pdf
        before_midday = request.POST.get("before_midday")
        meal_in_progress = MealSession.in_progress()
        status = status_code.HTTP_200_OK

        if before_midday:
            content = {"status": "Breakfast started"}
        else:
            content = {"lunch": "Lunch started"}

        timezone.activate(pytz.timezone("Africa/Lagos"))
        time = timezone.now()
        if not meal_in_progress.count():
            meal_in_progress = MealSession.objects.create(date=time.date(), status=True)
        else:
            meal_in_progress[0].status = True
            meal_in_progress[0].save()
        return Response(content, status=status)

    @guard
    @swagger_auto_schema()
    @action(methods=["post"], url_path="stop", detail=False)
    def stop(self, request):
        """
        A method that stops meal session.
        ---
        parameters:
            - name: before_midday
              description: is the time before or after 12 noon?
              required: true
              type: boolean
              paramType: form
            - name: passphrase
              description: passphrase to allow authentication
              required: true
              type: string
              paramType: form
        """
        before_midday = request.POST.get("before_midday")
        meal_in_progress = MealSession.in_progress()
        status = status_code.HTTP_200_OK

        if before_midday:
            content = {"status": "Breakfast stopped"}
        else:
            content = {"lunch": "Lunch stopped"}

        if meal_in_progress:
            meal_in_progress[0].status = False
            meal_in_progress[0].save()

        return Response(content, status=status)


class ReportViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for viewing reports on meal sessions.
    """

    queryset = MealService.objects.all()

    @swagger_auto_schema()
    def list(self, request):
        """
        A method that returns the reports for a meal service.\n
        * If the to query parameter is missing, the report is crammed until the present date.
        ---
        parameters:
            - name: from
              description: format yyyy-mm-dd or yyyy-mm
              required: false
              type: string
              paramType: query
            - name: to
              description: format yyyy-mm-dd
              required: false
              type: string
              paramType: query
        """
        date_today = timezone.now().date().strftime("%Y-%m-%d")
        start_date = request.GET.get("from", None)
        end_date = request.GET.get("to", None)
        queryset = self.queryset
        if start_date is None:
            queryset = self.queryset.filter(date__startswith=date_today)
        else:
            if len(start_date.split("-")) < 3:
                start_date = "{0}-{1}".format(start_date, "01")
                end_date = end_date if end_date is not None else date_today
            queryset = self.queryset.filter(date__range=[start_date, end_date])
        report = ReportSerializer.count(queryset)

        return Response(report, status_code.HTTP_200_OK)
