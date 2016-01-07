import os
from django.conf import settings
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

class HomeView(TemplateView):
    template_name = 'app/home.html'
