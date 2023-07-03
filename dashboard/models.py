from django.db import models

# Create your models here.
class StatLine(models.Model):

    player_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    points = models.IntegerField()

    def __str__(self): 
        return self.player_id
    
