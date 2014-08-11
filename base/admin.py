from django.contrib import admin
from base.models import *
from base.forms import AdvancedSearchForm
from django.forms.formsets import formset_factory
from django.db.models import Q
import re

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
    list_display = ('title', 'identifiers', 'descriptors')
    
    change_list_template = 'admin/base/change_list.html'
    change_form_template = 'admin/base/change_form.html'
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['advanced_formset'] = 'test for context'
        return super(SubjectAdmin, self).changelist_view(request, extra_context=extra_context)
        
    def get_search_results(self, request, queryset, search_term):
        '''Override the regular keyword search to perform the advanced search
        
        Because of the modified search_form.html template, the search_term will be specially
        generated to work with this method. Each set of queries is delimited by ??? and takes
        the form [&AND/OR]PROPERTY___SEARCH_TYPE___[SEARCH_KEYWORDS]??? This search method will 
        return inaccurate results if someone searches ??? as a keyword
        '''
        queryset, use_distinct = super(SubjectAdmin, self).get_search_results(request, queryset, search_term)

        query_rows = search_term.split('???') #list of queries from search_term

        # make sure we received list of queries
        if len(query_rows) > 0:
                   
            for i, row in enumerate(query_rows):
               
                negate = False # whether the query will be negated
                connector = '' # AND/OR/NOTHING
                
                terms = row.split('___')                
                
                if len(terms) >= 3:
                    # we got at least the number of terms we need

                    # CURRENT TERMS FORMAT: ([&AND/OR,] PROPERTY, [not_]SEARCH_TYPE, [SEARCH_KEYWORDS])
                
                    # remove and save the operator, if present
                    if terms[0].startswith('&'): 
                        connector = terms[0][1:]
                        terms = terms[1:]

                    # CURRENT TERMS FORMAT: (PROPERTY, [not_]SEARCH_TYPE, [SEARCH_KEYWORDS])
                        
                    # remove and save the negation, if present
                    if terms[1].startswith('not'):
                        negate = True
                        terms[1] = terms[1][4:]

                    # CURRENT TERMS FORMAT: (PROPERTY, SEARCH_TYPE, [SEARCH_KEYWORDS])
                    
                    ########### PROBLEM: THIS IS VERY DEPENDENT ON THE DATA AND UNUM REMAINING AT ID 23
                    # if search is for U Number, remove any non-numbers at the beginning
                    if terms[0] == 23:
                        d = re.search("\d", terms[2])
                        if d:
                            start_index = d.start()
                            terms[2] = terms[2][start_index:]
                    ###########

                    # create current query
                    kwargs = {str('subjectproperty__property_value__%s' % terms[1]) : str('%s' % terms[2])}
                    
                    # use negation
                    if negate:
                        current_query = Q(Q(subjectproperty__property = terms[0]) & ~Q(**kwargs))
                    else:
                        current_query = Q(Q(subjectproperty__property = terms[0]) & Q(**kwargs))
                    
                    # modify query set
                    if connector == 'AND':
                        queryset = queryset.filter(current_query)
                    elif connector == 'OR':
                        queryset = queryset | self.model.objects.filter(current_query)
                    else:
                        if i == 0:
                            # in this case, current query should be the first query, so no connector
                            queryset = self.model.objects.filter(current_query)
                        else:
                            # if connector wasn't set, use &
                            queryset = queryset.filter(current_query)
            
        return queryset.order_by('id'), use_distinct

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