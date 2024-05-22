from django.db import models

# Create your models here.
class Alerts(models.Model):
    rail = models.CharField(max_length=255, null = True)
    name = models.TextField(null=True)
    subject = models.CharField(max_length=255, null=True)
    date = models.CharField(max_length=255, null = True)
    content = models.TextField(null=True)

class Advisories(models.Model):
    name = models.TextField(null=True)
    subject = models.CharField(max_length=255, null = True)
    date = models.CharField(max_length=255, null = True)
    content = models.TextField(null = True)