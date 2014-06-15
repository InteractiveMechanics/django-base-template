from django import forms
from haystack.forms import ModelSearchForm
from base.models import DescriptiveProperty
from haystack.inputs import Raw
from haystack.query import SearchQuerySet

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