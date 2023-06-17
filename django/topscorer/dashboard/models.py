from django.db import models

from django.db import models


class StatLine(models.Model):
    player_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    points = models.IntegerField()
