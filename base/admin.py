from django.contrib import admin
from base.models import *

class SubjectPropertyInline(admin.TabularInline):
    model = SubjectProperty
    extra = 3
    fields = ['property', 'property_value', 'last_mod_by']

class SubjectAdmin(admin.ModelAdmin):
    fields = ['title', 'notes', 'last_mod_by']
    inlines = [SubjectPropertyInline]

admin.site.register(Subject, SubjectAdmin)

admin.site.register(GlobalVars)
admin.site.register(Media)
admin.site.register(MediaType)
admin.site.register(DescriptiveProperty)
admin.site.register(MediaProperty)
admin.site.register(FeaturedImgs)
admin.site.register(SubjectProperty)
admin.site.register(ResultProperty)
admin.site.register(Relations)
admin.site.register(PersonOrg)
admin.site.register(PersonOrgProperty)