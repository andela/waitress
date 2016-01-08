from app.utils import UserRepository, Time
from app.serializers import UserSerializer
from app.models import SlackUser, MealSession, MealService, Passphrase
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
import json
import pytz

class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = SlackUser.objects.all()

    def list(self, request):
        """
        A method that gets the list of users.
        """
        filter = request.GET.get('filter')
        queryset = self.queryset
        if request.GET.get('filter'):
            queryset = queryset.filter(firstname__startswith=filter)
        else:
            queryset = queryset.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='update-users')
    def update_users(self, request):
        """
        A method that updates the list of users.
        """
        status = UserRepository.update()
        content = {"status": status}

        return Response(content)

    @detail_route(methods=['post'], url_path='tap')
    def tap(self, request, pk):
        """
        A method that taps in a user.
        """
        content = {}
        meal_in_progress = MealSession.in_progress()
        user = get_object_or_404(self.queryset, pk=pk)
        if not meal_in_progress:
            content['status'] = 'There is no meal in progress'
        else:
            before_midday = Time.is_before_midday()
            date_today = meal_in_progress[0].date
            mealservice = MealService.objects.filter(user=user, date=date_today)

            if not mealservice.count():
                mealservice = MealService()
            else:
                mealservice = mealservice[0]

            if before_midday:
                mealservice.breakfast = True
            else:
                mealservice.lunch = True

            mealservice.user = user
            mealservice.date = date_today
            mealservice.date_modified = timezone.now()
            mealservice.save()
            content['status'] = 'Tap was successful'

        return Response(content)

    @detail_route(methods=['post'], url_path='untap')
    def untap(self, request, pk):
        """
        A method that untaps a user.
        """
        before_midday = Time.is_before_midday()
        content = {}
        meal_in_progress = MealSession.in_progress()
        passphrase = request.POST.get('passphrase')
        user = get_object_or_404(self.queryset, pk=pk)
        mealservice = MealService.objects.get(
                user=user, date=meal_in_progress[0].date
            )
        if not meal_in_progress:
            content['status'] = 'There is no meal in progress'
        else:
            passphrase = Passphrase.objects.filter(word=passphrase)
            if passphrase.count():
                if before_midday:
                    mealservice.breakfast = False
                else:
                    mealservice.lunch = False
                timenow = timezone.now()
                if not mealservice.untapped:
                    untapped = []
                else:
                    untapped = json.loads(mealservice.untapped)
                log = {
                        'date_untapped': str(timenow),
                        'user': passphrase[0].user.id
                    }
                untapped.append(log)
                mealservice.untapped = untapped
                mealservice.date_modified = timenow
                mealservice.save()
                content['status'] = 'Untap was successful'
            else:
                content = {'status': 'Invalid passphrase'}
        return Response(content)


class MealSessionViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving meal session.
    """

    queryset = MealSession.objects.all()

    def list(self, request):
        """
        A method that tells if time is before mid-day.
        """
        before_midday = Time.is_before_midday()
        content = {'before_midday': before_midday}

        return Response(content)

    @list_route(methods=['post'], url_path='start')
    def start(self, request):
        """
        A method that starts meal session.
        """
        before_midday = request.POST.get('before_midday')
        meal_in_progress = MealSession.in_progress().count()
        passphrase = request.POST.get('passphrase')
        if before_midday:
            content = {'status': 'Breakfast started'}
        else:
            content = {'lunch': 'Lunch started'}

        if Passphrase.objects.filter(word=passphrase).count():
            timezone.activate(pytz.timezone('Africa/Lagos'))
            time = timezone.now()
            if not meal_in_progress:
                MealSession.objects.create(date=time.date(), status=True)
        else:
            content = {'status': 'Invalid passphrase'}
        return Response(content)

    @list_route(methods=['post'], url_path='stop')
    def stop(self, request):
        """
        A method that stops meal session.
        """
        before_midday = request.POST.get('before_midday')
        meal_in_progress = MealSession.in_progress()
        passphrase = request.POST.get('passphrase')
        if before_midday:
            content = {'status': 'Breakfast stopped'}
        else:
            content = {'lunch': 'Lunch stopped'}

        if Passphrase.objects.filter(word=passphrase).count():
            if meal_in_progress:
                meal_in_progress[0].status = False
                meal_in_progress[0].save()
        else:
            content = {'status': 'Invalid passphrase'}
        return Response(content)
