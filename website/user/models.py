from django.db import models

class Log(models.Model):
    date = models.DateTimeField('date published')
    pourcent = models.IntegerField(default=0)