""" Basic models, such as user profile """
from django.db import models

class GlobalVars(models.Model):
    variable = models.CharField(max_length = 200)
    val = models.TextField()
	
    def __unicode__(self):
        return self.val  