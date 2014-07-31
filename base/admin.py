from django.contrib import admin
from base.models import *
from base.forms import AdvancedSearchForm
from django.forms.formsets import formset_factory

class PropertyFilter(admin.SimpleListFilter):

    title = 'property'
    
    parameter_name = 'prop'
    
    def lookups(self, request, model_admin):
        properties = tuple((prop.id, prop.property) for prop in DescriptiveProperty.objects.all())    
        return properties

    def queryset(self, request, queryset):
        if self.value():
            prop_id = self.value()
            return queryset.filter(subjectproperty__property = prop_id)

class SubjectPropertyInline(admin.TabularInline):
    model = SubjectProperty
    extra = 3
    fields = ['property', 'property_value', 'last_mod_by']

class SubjectAdmin(admin.ModelAdmin):
    fields = ['title', 'notes', 'last_mod_by']
    inlines = [SubjectPropertyInline]
    search_fields = ['title']
    list_display = ('title', 'get_unum')
    
    change_list_template = 'admin/base/change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['advanced_formset'] = 'test for context'
        return super(SubjectAdmin, self).changelist_view(request, extra_context=extra_context)
        

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
admin.site.register(MediaSubjectRelations)
admin.site.register(MediaPersonOrgRelations)
admin.site.register(PersonOrgProperty)