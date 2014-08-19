from django import forms
from haystack.forms import ModelSearchForm, SearchForm
from base.models import DescriptiveProperty
from haystack.inputs import Raw
from haystack.query import SearchQuerySet

OPERATOR = (
    ('and', 'AND'),
    ('or', 'OR'),
    ('not', 'NOT'),
)

SEARCH_TYPE = (
    ('contains', 'contains'),
    ('like', 'like'),
    ('exact', 'equals'),
    ('startswith', 'starts with'),
    ('endswith', 'ends with'),
    ('blank', 'is blank'),
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
    search_type = forms.ChoiceField(required=False, choices=SEARCH_TYPE)
    q = forms.CharField(required=False)
    
    def search(self):
        
        if not self.is_valid():
            return self.no_query_found()

        prop = 'content'
        type = 'contains' #give this a value just in case
            
        # A property was selected
        if self.cleaned_data['property'] != None:
            prop = 'prop_'+ str(self.cleaned_data['property'].id)
            co
        # Determine the type of search
        if self.cleaned_data['search_type'] == 'like':
            pass #FIX THIS
        
        elif self.cleaned_data['search_type'] == 'blank':
            pass #FIX THIS
            
        elif self.cleaned_data['search_type'] == 'endswith':
            pass #FIX THIS
            
        else:
            type = self.cleaned_data['search_type']
            
        kwargs = {str('%s__%s' % (prop, type)) : str('%s' % self.cleaned_data['q'])}
        sqs = SearchQuerySet().filter(**kwargs)

        return sqs
