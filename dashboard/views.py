# dashboard, views.py

from django.shortcuts import render
from django.http import HttpResponse


def Dashboard(render):
    return HttpResponse('Dashboard')