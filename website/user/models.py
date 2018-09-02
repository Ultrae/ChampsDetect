from django.db import models

class Log(models.Model):
    date = models.DateTimeField('date published')
    description = models.CharField(max_length=500, default="")
    pourcent = models.IntegerField(default=0)