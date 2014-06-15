from django.contrib import admin
from base.models import *

class SubjectPropertyInline(admin.TabularInline):
    model = SubjectProperty
    extra = 3
    fields = ['property', 'property_value', 'last_mod_by']

class SubjectAdmin(admin.ModelAdmin):
    fields = ['title', 'notes', 'last_mod_by']
    inlines = [SubjectPropertyInline]
    search_fields = ['title']

admin.site.register(Subject, SubjectAdmin)

class MediaPropertyInline(admin.TabularInline):
    model = MediaProperty
    extra = 3
    fields = ['property', 'property_value', 'last_mod_by']

class MediaAdmin(admin.ModelAdmin):
    fields = ['title', 'notes', 'last_mod_by']
    inlines = [MediaPropertyInline]
    search_fields = ['title']
    
admin.site.register(Media, MediaAdmin)

class PersonOrgPropertyInline(admin.TabularInline):
    model = PersonOrgProperty
    extra = 3
    fields = ['property', 'property_value', 'last_mod_by']

class PersonOrgAdmin(admin.ModelAdmin):
    fields = ['title', 'notes', 'last_mod_by']
    inlines = [PersonOrgPropertyInline]
    search_fields = ['title']

admin.site.register(PersonOrg, PersonOrgAdmin)

admin.site.register(GlobalVars)
admin.site.register(MediaType)
admin.site.register(DescriptiveProperty)
admin.site.register(MediaProperty)
admin.site.register(FeaturedImgs)
admin.site.register(SubjectProperty)
admin.site.register(ResultProperty)
admin.site.register(Relations)
admin.site.register(PersonOrgProperty)