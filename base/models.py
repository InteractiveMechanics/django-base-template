""" Basic models, such as user profile """
from django.db import models
from django.contrib.auth.models import User

class GlobalVars(models.Model):
    variable = models.CharField(max_length = 200)
    val = models.TextField()
	
    def __unicode__(self):
        return self.variable

class MediaType(models.Model):
    type = models.CharField(max_length = 40)

    def __unicode__(self):
        return self.type    
        
class Media(models.Model):
    title = models.CharField(max_length = 100)
    type = models.ForeignKey(MediaType)
    featured = models.BooleanField(default = False)
    uri = models.URLField(blank = True)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title