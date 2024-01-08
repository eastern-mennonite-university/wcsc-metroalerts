from django.db import models

# Create your models here.
class Alerts(models.Model):
    name = models.CharField(max_length=255, null=True)
    subject = models.CharField(max_length=255)
    date = models.DateField(null = True)
    content = models.CharField(max_length=255)

class Advisories(models.Model):
    name = models.CharField(max_length=255, null=True)
    subject = models.CharField(max_length=255)
    date = models.DateField(null = True)
    content = models.CharField(max_length=255)