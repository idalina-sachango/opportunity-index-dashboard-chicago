from django.shortcuts import render
from django.http import HttpResponse
from .models import cps

def index(request):
    return HttpResponse("Hello, world. You're looking at tools4schools.")

def default_map(request):
    return render(request, 'default.html', {})
