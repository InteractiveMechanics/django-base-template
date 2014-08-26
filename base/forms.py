from django import forms
from haystack.forms import ModelSearchForm, SearchForm
from base.models import DescriptiveProperty
from haystack.inputs import Raw
from haystack.query import SearchQuerySet
import re

OPERATOR = (
    ('and', 'AND'),
    ('or', 'OR'),
    ('not', 'NOT'),
)

SEARCH_TYPE = (
    ('contains', 'contains'),
    ('!contains', 'does not contain'),
    ('like', 'like'),
    ('!like', 'is not like'),
    ('exact', 'equals'),
    ('!exact', 'does not equal'),
    ('blank', 'is blank'),
    ('!blank', 'is not blank'),
    ('startswith', 'starts with'),
    ('!startswith', 'does not start with'),
    ('endswith', 'ends with'),
    ('!endswith', 'does not end with'),
    ('gt', 'is greater than'),
    ('gte', 'is greater than or equal to'),
    ('lt', 'is less than'),
    ('lte', 'is less than or equal to'),
)

class PropertySelectorSearchForm(ModelSearchForm):
    property = forms.ModelChoiceField(required=False, label=('Property'), queryset=DescriptiveProperty.objects.all(), empty_label="Any")
    q = forms.CharField(required=False, label=(''), widget=forms.TextInput(attrs={'type': 'search'}))
    
    def __init__(self, *args, **kwargs):
        super(PropertySelectorSearchForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [ 'property', 'q' , 'models']
        
    def no_query_found(self):
        return self.searchqueryset.all()
        
    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PropertySelectorSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()
            
        if self.cleaned_data['property'] != None:
            prop = self.cleaned_data['property']
        
            sqs = SearchQuerySet().filter(content=Raw('prop_' + str(prop.id) + ':' + self.cleaned_data['q']))
        
        return sqs
        
class AdvancedSearchForm(SearchForm):
    property = forms.ModelChoiceField(required=False, queryset=DescriptiveProperty.objects.all(), empty_label="Any")
    search_type = forms.ChoiceField(label='', required=False, choices=SEARCH_TYPE)
    q = forms.CharField(label='Search Terms', required=False)
    
    def __init__(self, *args, **kwargs):
        super(AdvancedSearchForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['property', 'search_type', 'q']
    
    def search(self):
        
        if not self.is_valid():
            return self.no_query_found()

        prop = 'content'
        type = self.cleaned_data['search_type']
        query = self.cleaned_data['q']
        negate = False
        kwargs = {}
            
        # A property was selected
        if self.cleaned_data['property'] != None:
            prop = 'prop_'+ str(self.cleaned_data['property'].id)
            
        # Check for not
        if type.startswith('!'):
            negate = True
            type = type[1:]
            
        # Determine the type of search
            
        # CONTAINS -> special case misspellings
        if type == 'contains':
        
            add_or = False
        
            query_text = '('
        
            # special misspellings
            if prop == 'prop_23':
                #if doing a contains search for u number, get first instance of numbers followed by a 0 or 1 letter
                match = re.search(r'(\d+[a-zA-Z]?)', query)
                if match:
                    query = match.group(0)
                    query_text += ('' + query + '?')
                    add_or = True
            else:
                query = re.sub(r'(\s*)([uU]\s*?\.?\s*)(\d+)([a-zA-Z]*)', r'\1u* *\3*', query)
                query = re.sub(r'(\s*)([pP][gG]\s*?\.?\s*)(\w+)', r'\1pg* *\3*', query)
            
            keywords = query.split()
            
            if keywords:
                
                if add_or:
                    query_text += ' OR '
            
                query_text += '('
            
                for i, word in enumerate(keywords):
                    
                    if i > 0: 
                        query_text += ' AND '
                    query_text += word
                
                query_text += '))'
                
                kwargs = {str('%s' % prop) : Raw(query_text)}
            
            else:
                return SearchQuerySet().all()            
        
        # LIKE -> 'a*b' or 'a?b'
        elif type == 'like':
        
            keywords = query.split()
            
            if keywords:
                query_text = '('
            
                for i, word in enumerate(keywords):
                    
                    if i > 0: 
                        query_text += ' AND '
                    query_text += word
                
                query_text += ')'
                
                kwargs = {str('%s' % prop) : Raw(query_text)}
            
            else:
                return SearchQuerySet().all()
        
        # BLANK -> returns all subjects that don't have a value for given property
        elif type == 'blank':
            
            #if property is Any, then return all b/c query asks for doc with 'any' blank properties
            if self.cleaned_data['property'] == None:
                return SearchQuerySet().all()
                
            # BLANK is a special case negation (essentially a double negative), so handle differently
            if negate:
                kwargs = {str('%s' % prop) : Raw('[1 TO *]')}
                negate = False
            else:
                kwargs = {str('-%s' % prop) : Raw('[* TO *]')}
            
        # ENDSWITH -> '*abc'
        elif type == 'endswith':
        
            keywords = query.split()
            
            if keywords:
                query_text = '('
            
                for i, word in enumerate(keywords):
                    
                    if i > 0: 
                        query_text += ' AND '
                    query_text += ('*' + word)
                
                query_text += ')'
                
                kwargs = {str('%s' % prop) : Raw(query_text)}
                
            else:
                return SearchQuerySet().all()
            
        else:
        
            # no search terms given, so return everything
            if query == '':
                return SearchQuerySet().all()
            
            kwargs = {str('%s__%s' % (prop, type)) : str('%s' % query)}
       
        if negate:
            sqs = SearchQuerySet().exclude(**kwargs)
        else:
            sqs = SearchQuerySet().filter(**kwargs)

        return sqs
