from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Alerts, Advisories

# Create your views here.
def main(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def alerts(request):
    walerts = Alerts.objects.all().values()

def advisories(request):
    wadvisories = Advisories.objects.all().values()