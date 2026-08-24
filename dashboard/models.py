from django.db import models

class ScoreTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    player_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    points = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'score_table'