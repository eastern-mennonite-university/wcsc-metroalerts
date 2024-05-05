from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Alerts, Advisories

# Create your views here.
def main(request):
    return render(request, 'index.html', {
        "alerts_list": Alerts.objects.all(),
        "advisories_list": Advisories.objects.all()
    })
'''
def check_database_updates(request):
    #Retrieve data from the database
    new_items = Alerts.objects.filter(is_processed=False)

    #Process new items if needed
    for item in new_items:
        item.is_processed = True
        item.save()
'''