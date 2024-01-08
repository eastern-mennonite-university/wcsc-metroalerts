from django.contrib import admin
from .models import Alerts, Advisories
# Register your models here.
admin.site.register(Alerts)
admin.site.register(Advisories)