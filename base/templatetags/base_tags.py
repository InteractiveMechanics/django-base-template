from django import template
from django.core.urlresolvers import reverse
from base.models import GlobalVars, ResultProperty, DescriptiveProperty, MediaSubjectRelations, MediaPersonOrgRelations, Subject
from django.contrib.admin.templatetags.admin_list import result_list
from django.db.models import Q
import re
from django.contrib.admin.views.main import (ALL_VAR, EMPTY_CHANGELIST_VALUE,
    ORDER_VAR, PAGE_VAR, SEARCH_VAR)

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    """ Returns "active" if the current request is for the givens urls. 
        Used by the nav menus to highlight the active tab. """

    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag    
def load_globals(key):
    """ Returns the value of a global variable """

    global_var = GlobalVars.objects.get(variable = key)

    return global_var.val
    
@register.simple_tag    
def load_result_display_fields(fields, key):
    """ Selects the field to be displayed in result list """

    prop_list = []
    
    if key.endswith('title'):
        for i in range(3):
            title_str = key + str(i + 1)
            title = ResultProperty.objects.get(display_field = title_str)
            if title.field_type:
                p = 'prop_' + str(title.field_type.id)
                property_name = title.field_type.property
                value = fields.get(p, '')
                if value != '' :
                    prop_list.append(property_name + ' : ' + str(fields.get(p, '')))
    else:
        prop = ResultProperty.objects.get(display_field = key)
        if prop.field_type:
            prop_id = prop.field_type.id
            p = 'prop_' + str(prop_id)
            try:
                prop_list.append(fields.get(p, ''))
            except TypeError:
                prop_list.append(str(fields.get(p, '')))
    
    prop_str = ''
    
    for p in prop_list:
        prop_str += (p + '<br>')
 
    return prop_str
        
@register.simple_tag    
def get_query_params(request):
    str = ''
    
    keys = ['property', 'q', 'models']
    
    for key in keys:
        if key in request:
            param = key + '=' + request[key] + '&amp;'
            str += param
    
    return str
    
@register.simple_tag    
def get_result_details(fields):
    rowhtml = ''

    for field, value in fields.items():
        if field.startswith('prop_'):
            prop_num = field[5:]
            try:
                prop = DescriptiveProperty.objects.get(id=prop_num)
                try:
                    row = '<tr><td>' + prop.property + '</td><td>' + value + '</td></tr>'
                except TypeError:
                    row = '<tr><td>' + prop.property + '</td><td>' + str(value) + '</td></tr>'              
                rowhtml += row
            except DescriptiveProperty.DoesNotExist:
                pass
            
    return rowhtml
    
@register.simple_tag    
def get_img_thumb(object):
    relation = MediaSubjectRelations.objects.filter(subject = object.id)
    
    if relation:
        first_rel = relation[0]
        uri_prop = first_rel.media.mediaproperty_set.filter(property__property = 'URI')
        if uri_prop:
            return uri_prop[0].property_value
    
    return 'http://ur.iaas.upenn.edu/static/img/no_img.jpg'
    
@register.simple_tag    
def get_img_thumb_po(object):
    relation = MediaPersonOrgRelations.objects.filter(person_org = object.id)
    
    if relation:
        first_rel = relation[0]
        uri_prop = first_rel.media.mediaproperty_set.filter(property__property = 'URI')
        if uri_prop:
            return uri_prop[0].property_value
    
    return 'http://ur.iaas.upenn.edu/static/img/no_img.jpg'
    
@register.simple_tag
def get_properties_dropdown():
    props = DescriptiveProperty.objects.all()
    options = '<option value="0">Any</option>'
    for prop in props:
        option = '<option value="' + str(prop.id) + '">' + prop.property + '</option>'
        options += option
        
    return options
    
@register.simple_tag
def load_last_query(query):
    types = {'icontains': 'contains', 'not_icontains': 'does not contain', 'istartswith': 'starts with', 'iendswith': 'ends with', 'blank': 'is blank', 'not_blank': 'is not blank', 'exact': 'equals', 'not_exact': 'is not equal', 'gt': 'is greater than', 'gte': 'is greater than or equal to', 'lt': 'is less than', 'lte': 'is less than or equal to'}

    query_rows = query.split('???')
    
    display_text = ''
    
    for row in query_rows:
        terms = row.split('___')
        
        if len(terms) >= 3:
        
            if terms[0].startswith('&'):
                display_text += (' '  + terms[0][1:])
                terms = terms[1:]
        
            # if a property is searched for that doesn't exist, set property to Any
            prop = 'Any'
            try:
                prop = DescriptiveProperty.objects.get(pk=terms[0])
            except DescriptiveProperty.DoesNotExist:
                pass
            display_text += (' (' + prop.property)
            display_text += (' ' + types[terms[1]])
            display_text += (' ' + terms[2] + ')')
        
    return display_text
    
@register.simple_tag
def advanced_obj_search(search_term):

    cleaned_search_term = search_term[2:]

    query_rows = cleaned_search_term.split('%3F%3F%3F') #list of queries from search_term
    
    queryset = Subject.objects.all()

    # make sure we received list of queries
    if len(query_rows) > 0:
               
        for i, row in enumerate(query_rows):
           
            negate = False # whether the query will be negated
            connector = '' # AND/OR/NOTHING
            kwargs = {}
            current_query = Q()            
            
            terms = row.split('___')                
            
            if len(terms) >= 3:
                # we got at least the number of terms we need

                # CURRENT TERMS FORMAT: ([&AND/OR,] PROPERTY, [not_]SEARCH_TYPE, [SEARCH_KEYWORDS])
            
                # remove and save the operator, if present
                if terms[0].startswith('%26'): 
                    connector = terms[0][3:]
                    terms = terms[1:]

                # CURRENT TERMS FORMAT: (PROPERTY, [not_]SEARCH_TYPE, [SEARCH_KEYWORDS])
                    
                # remove and save the negation, if present
                if terms[1].startswith('not'):
                    negate = True
                    terms[1] = terms[1][4:]

                # CURRENT TERMS FORMAT: (PROPERTY, SEARCH_TYPE, [SEARCH_KEYWORDS])
                
                # if this row is blank, than skip
                if (terms[2] == '') and (terms[1] != 'blank'):
                    continue
                    
                ########### PROBLEM: THIS IS VERY DEPENDENT ON THE DATA AND UNUM REMAINING AT ID 23
                # if search is for U Number, remove any non-numbers at the beginning
                if terms[0] == '23':
                    d = re.search("\d", terms[2])
                    if d is not None:
                        start_index = d.start()
                        terms[2] = terms[2][start_index:]
                ###########
                
                # create current query
                if terms[1] == 'blank':
                    #if property is Any, then return all b/c query asks for doc with 'any' blank properties
                    if terms[0] == '0':
                        continue
                        
                    # BLANK is a special case negation (essentially a double negative), so handle differently
                    if negate:
                        current_query = Q(subjectproperty__property = terms[0])
                    else:
                        current_query = ~Q(subjectproperty__property = terms[0])                   
                
                else:
                    kwargs = {str('subjectproperty__property_value__%s' % terms[1]) : str('%s' % terms[2])}

                    # check if a property was selected and build the current query
                    if terms[0] == '0':
                        # if no property selected, than search thru ALL properties
                        # use negation
                        if negate:
                            current_query = ~Q(**kwargs)
                        else:
                            current_query = Q(**kwargs)
                    else:
                        # use negation
                        if negate:
                            current_query = Q(Q(subjectproperty__property = terms[0]) & ~Q(**kwargs))
                        else:
                            current_query = Q(Q(subjectproperty__property = terms[0]) & Q(**kwargs))
  
                # modify query set
                if connector == 'AND':
                    queryset = queryset.filter(current_query)
                elif connector == 'OR':
                    queryset = queryset | Subject.objects.filter(current_query)
                else:
                    if i == 0:
                        # in this case, current query should be the first query, so no connector
                        queryset = Subject.objects.filter(current_query)
                    else:
                        # if connector wasn't set, use &
                        queryset = queryset.filter(current_query)
        
    return queryset.order_by('id').distinct()
    
@register.filter
def get_next(value, arg):

    terms = value.GET.get('_changelist_filters')
    
    if terms:
        queryset = advanced_obj_search(terms)
    
        remaining_objects = queryset.filter(id__gt=arg).order_by('id')
    
        if remaining_objects:
            return remaining_objects[0].id
    
    return ''
    
@register.filter
def has_next(value, arg):
    
    terms = value.GET.get('_changelist_filters')

    if terms:
        queryset = advanced_obj_search(terms)
        
        remaining_objects = queryset.filter(id__gt = arg).order_by('id')[:1]
        
        if remaining_objects:
            return True
        else:
            return True

    return False
    
@register.filter
def get_prev(value, arg):

    terms = value.GET.get('_changelist_filters')
    
    if terms:
        queryset = advanced_obj_search(terms)
    
        remaining_objects = queryset.filter(id__lt=arg).order_by('-id')
    
        if remaining_objects:
            return remaining_objects[0].id
    
    return ''
    
@register.filter
def has_prev(value, arg):
    
    terms = value.GET.get('_changelist_filters')

    if terms:
        queryset = advanced_obj_search(terms)
        
        remaining_objects = queryset.filter(id__lt = arg).order_by('-id')[:1]
        
        if remaining_objects:
            return True
        else:
            return True

    return False
    
@register.filter
def get_filter_param(value):
    return value.GET.get('_changelist_filters')
    
@register.simple_tag
def get_params_list(query, index):
    
    params = re.split(r"\?{3}|_{3}", query)
    
    if len(params) >= index + 1:
        return params[index]
    
    return ''
    
@register.inclusion_tag('admin/base/subject/search_form.html')
def subject_search_form(cl):
    """
    Displays a search form for searching the list.
    """
    return {
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR
    }