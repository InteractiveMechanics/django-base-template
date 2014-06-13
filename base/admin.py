from django.contrib import admin
from base.models import GlobalVars, Media, MediaType, DescriptiveProperty, MediaProperty, Subject, SubjectProperty, FeaturedImgs

admin.site.register(GlobalVars)
admin.site.register(Media)
admin.site.register(MediaType)
admin.site.register(DescriptiveProperty)
admin.site.register(MediaProperty)
admin.site.register(FeaturedImgs)
admin.site.register(Subject)
admin.site.register(SubjectProperty)