from app.decorators import guard
from app.models import SlackUser, MealSession, MealService
from app.serializers import UserSerializer, SecureUserSerializer,\
    ReportSerializer
from app.utils import UserRepository, Time
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status as status_code, viewsets
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
            queryset = queryset.filter(
                firstname__startswith=filter
            ).order_by('firstname')
        else:
            queryset = queryset.all()
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data, status_code.HTTP_200_OK)

    @guard
    @detail_route(methods=['post'], url_path='retrieve-secure')
    def retrieve_securely(self, request, pk):
        """
        A method that gets the detail of a user.
        """
        queryset = get_object_or_404(self.queryset, pk=pk)
        serializer = SecureUserSerializer(queryset)
        return Response(serializer.data, status_code.HTTP_200_OK)

    @list_route(methods=['get'], url_path='update-users')
    def update_users(self, request):
        """
        A method that updates the list of users.
        """
        status = UserRepository.update()
        content = {"status": status}
        return Response(content, status_code.HTTP_200_OK)

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
            mealservice = MealService.objects.filter(
                user=user, date=date_today
            ).order_by('firstname')

            if not mealservice.count():
                mealservice = MealService()
            else:
                mealservice = mealservice[0]

            mealservice = mealservice.set_meal(before_midday)

            mealservice = mealservice.set_user_and_date(user, date_today)
            mealservice.save()
            content['status'] = 'Tap was successful'

        return Response(content, status=status_code.HTTP_200_OK)

    @list_route(methods=['post'], url_path='nfctap')
    def nfctap(self, request):
        """
        A method that taps a user via an NFC card.
        """
        slack_id = request.POST.get('slackUserId')

        if not slack_id:
            content = {'status': 'You\'re  unauthorized to make this request'}
            return Response(content, status=status_code.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(self.queryset, slack_id=slack_id)
        meal_in_progress = MealSession.in_progress()
        content = {'firstname': user.firstname, 'lastname': user.lastname}
        if not meal_in_progress:
            content['status'] = 'There is no meal in progress'
        else:
            before_midday = Time.is_before_midday()
            date_today = meal_in_progress[0].date
            mealservice = MealService.objects.filter(
                user=user, date=date_today
            )

            if not mealservice.count():
                mealservice = MealService()
            else:
                mealservice = mealservice[0]

            mealservice = mealservice.set_meal(before_midday)
            mealservice = mealservice.set_user_and_date(user, date_today)
            mealservice.save()

            content['status'] = 'Tap was successful'

        return Response(content, status=status_code.HTTP_200_OK)

    @guard
    @detail_route(methods=['post'], url_path='untap')
    def untap(self, request, pk):
        """
        A method that untaps a user.
        """
        before_midday = Time.is_before_midday()
        content = {}
        meal_in_progress = MealSession.in_progress()
        timenow = timezone.now()
        user = get_object_or_404(self.queryset, pk=pk)
        mealservice = MealService.objects.get(
                user=user, date=meal_in_progress[0].date
            )
        status = status_code.HTTP_200_OK

        if not meal_in_progress:
            content['status'] = 'There is no meal in progress'
        else:
            mealservice = mealservice.set_meal(before_midday, reverse=True)
            if not mealservice.untapped:
                untapped = []
            else:
                untapped = json.loads(mealservice.untapped)
            log = {
                    'date_untapped': str(timenow),
                    'user': request.passphrase.user.id
                }
            untapped.append(log)
            mealservice.untapped = untapped
            mealservice.date_modified = timenow
            mealservice.save()
            content['status'] = 'Untap was successful'

        return Response(content, status=status)


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

        return Response(content, status=status_code.HTTP_200_OK)

    @guard
    @list_route(methods=['post'], url_path='start')
    def start(self, request):
        """
        A method that starts meal session.
        """
        before_midday = request.POST.get('before_midday')
        meal_in_progress = MealSession.in_progress()
        status = status_code.HTTP_200_OK
        if before_midday:
            content = {'status': 'Breakfast started'}
        else:
            content = {'lunch': 'Lunch started'}

        timezone.activate(pytz.timezone('Africa/Lagos'))
        time = timezone.now()
        if not meal_in_progress.count():
            meal_in_progress = MealSession.objects.create(
                date=time.date(), status=True
            )
        else:
            meal_in_progress[0].status = True
            meal_in_progress[0].save()
        return Response(content, status=status)

    @guard
    @list_route(methods=['post'], url_path='stop')
    def stop(self, request):
        """
        A method that stops meal session.
        """
        before_midday = request.POST.get('before_midday')
        meal_in_progress = MealSession.in_progress()
        status = status_code.HTTP_200_OK

        if before_midday:
            content = {'status': 'Breakfast stopped'}
        else:
            content = {'lunch': 'Lunch stopped'}

        if meal_in_progress:
            meal_in_progress[0].status = False
            meal_in_progress[0].save()

        return Response(content, status=status)


class ReportViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for viewing reports on meal sessions.
    """
    queryset = MealService.objects.all()

    def list(self, request):
        """
        A method that returns the reports for a meal service.
        """
        date_today = timezone.now().date().strftime('%Y-%m-%d')
        start_date = request.GET.get('from', None)
        end_date = request.GET.get('to', None)
        queryset = self.queryset
        if start_date is None:
            queryset = self.queryset.filter(date__startswith=date_today)
        else:
            if len(start_date.split('-')) < 3:
                start_date = '{0}-{1}'.format(start_date, '01')
                end_date = end_date if end_date is not None else date_today
            queryset = self.queryset.filter(date__range=[start_date, end_date])
        report = ReportSerializer.count(queryset)

        return Response(report, status_code.HTTP_200_OK)
