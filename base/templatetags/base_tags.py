from django import template
from django.core.urlresolvers import reverse
from base.models import GlobalVars, ResultProperty, DescriptiveProperty

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

    prop = ResultProperty.objects.get(display_field = key)
    prop_id = prop.field_type.id
    
    return fields.get(('prop_' + str(prop_id)), '')
    
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
            prop = DescriptiveProperty.objects.get(id=prop_num)
            row = '<tr><td>' + prop.property + '</td><td>' + str(value) + '</td></tr>'
            rowhtml += row
            
    return rowhtml