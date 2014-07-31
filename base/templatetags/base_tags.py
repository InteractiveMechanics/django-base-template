from django import template
from django.core.urlresolvers import reverse
from base.models import GlobalVars, ResultProperty, DescriptiveProperty, MediaSubjectRelations, MediaPersonOrgRelations
from django.contrib.admin.templatetags.admin_list import result_list

register = template.Library()
register.inclusion_tag('admin/base/expanded_change_list_results.html')(result_list)

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
                value = str(fields.get(p, ''))
                if value != '' :
                    prop_list.append(property_name + ' : ' + str(fields.get(p, '')))
    else:
        prop = ResultProperty.objects.get(display_field = key)
        if prop.field_type:
            prop_id = prop.field_type.id
            p = 'prop_' + str(prop_id)
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
            prop = DescriptiveProperty.objects.get(id=prop_num)
            row = '<tr><td>' + prop.property + '</td><td>' + str(value) + '</td></tr>'
            rowhtml += row
            
    return rowhtml
    
@register.simple_tag    
def get_img_thumb(object):
    relation = MediaSubjectRelations.objects.filter(subject = object.id)
    
    if relation:
        first_rel = relation[0]
        uri_prop = first_rel.media.mediaproperty_set.get(property__property = 'URI')
        return uri_prop.property_value
    
    return 'http://ur.iaas.upenn.edu/static/img/no_img.jpg'
    
@register.simple_tag    
def get_img_thumb_po(object):
    relation = MediaPersonOrgRelations.objects.filter(person_org = object.id)
    
    if relation:
        first_rel = relation[0]
        uri_prop = first_rel.media.mediaproperty_set.get(property__property = 'URI')
        return uri_prop.property_value
    
    return 'http://ur.iaas.upenn.edu/static/img/no_img.jpg'
    
@register.simple_tag
def get_properties_dropdown():
    props = DescriptiveProperty.objects.all()
    options = ''
    for prop in props:
        option = '<option value="' + str(prop.id) + '">' + prop.property + '</option>'
        options += option
        
    return options