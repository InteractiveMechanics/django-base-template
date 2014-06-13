from django.db import models
from django.contrib.auth.models import User

"""Variables used by pages throughout the site"""
class GlobalVars(models.Model):
    variable = models.CharField(max_length = 200)
    val = models.TextField()
	
    def __unicode__(self):
        return self.variable + self.val
        
"""Featured images for home page"""
class FeaturedImgs(models.Model):
    uri = models.URLField()
    description = models.CharField(max_length = 200)

"""Types of Media, such as image/jpeg, text/html, etc"""
class MediaType(models.Model):
    type = models.CharField(max_length = 40)

    def __unicode__(self):
        return self.type    

"""Types of descriptive properties (or variables to describe objects)"""
class DescriptiveProperty(models.Model):
    property = models.CharField(max_length = 60)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)    

    def __unicode__(self):
        return self.property         
        
"""Files that help make up documentation for project"""        
class Media(models.Model):
    title = models.CharField(max_length = 100)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title

"""Descriptive Properties of Media Files"""        
class MediaProperty(models.Model):
    media = models.ForeignKey(Media)
    property = models.ForeignKey(DescriptiveProperty)
    property_value = models.TextField()
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)   

    def __unicode__(self):
        return self.property_value
        
"""Primary subjects of observation for a project, usually objects or locations"""        
class Subject(models.Model):
    title = models.CharField(max_length = 100)
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title

"""Descriptive Properties of Subjects"""        
class SubjectProperty(models.Model):
    subject = models.ForeignKey(Subject)
    property = models.ForeignKey(DescriptiveProperty)
    property_value = models.TextField()
    notes = models.TextField(blank = True)
    created = models.DateTimeField(auto_now = False, auto_now_add = True)
    modified = models.DateTimeField(auto_now = True, auto_now_add = False)
    last_mod_by = models.ForeignKey(User)   

    def __unicode__(self):
        return self.property_value