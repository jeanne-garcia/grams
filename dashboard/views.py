# dashboard, views.py

from django.shortcuts import render
from django.http import HttpResponse


def Dashboard(request):
    return render(request, 'dashboard.html', {'title': 'Dashboard'})