from app.models import MealSession
from django.conf import setting
from django.utils import timezone
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import os
import pytz


class HomeView(TemplateView):
    template_name = 'app/home.html'


class SessionsView(View):
    """Show session"""
    def get(self, request):
        context_data = {}
        timezone.activate(pytz.timezone('Africa/Lagos'))
        time = timezone.now().hour
        if 0 < time < 12:
            if not MealSession.in_progress:
                context_data['before_midday'] = True
        else:
            context_data['before_midday'] = False
        return render(request, 'app/index.html', context_data)


class SessionView(View):
    """Start or end a session"""
    def get(self, request):
        context_data = {}
        return render(request, 'app/section.html', context_data)
