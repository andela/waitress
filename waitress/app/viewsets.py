from app.utils import UserRepository
from app.serializers import UserSerializer
from app.models import SlackUser, MealSession
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
import pytz


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = SlackUser.objects.all()

    def list(self, request):
        filter = request.GET.get('filter')
        queryset = SlackUser.objects.all()
        if request.GET.get('filter'):
            queryset = queryset.filter(name__startswith=filter)
        else:
            queryset = queryset.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='update-users')
    def update_users(self, request):
        status = UserRepository.update()
        content = {"status": status}

        return Response(content)

    def retrieve(self, request, pk=None):
        queryset = SlackUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class MealSessionViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving meal session.
    """

    queryset = MealSession.objects.all()

    def list(self, request):
        content = {}
        timezone.activate(pytz.timezone('Africa/Lagos'))
        time = timezone.now().hour
        if 0 < time < 12:
            if not MealSession.in_progress:
                content['before_midday'] = True
        else:
            content['before_midday'] = False
        return Response(content)
