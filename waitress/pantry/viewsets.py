from datetime import date

from rest_framework import status as status_code
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import SlackUser, Passphrase

from pantry.models import Pantry


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

