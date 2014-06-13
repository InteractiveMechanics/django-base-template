from django import forms
from haystack.forms import SearchForm
from base.models import DescriptiveProperty

class PropertySelectorSearchForm(SearchForm):
    property = forms.ModelChoiceField(required=False, label=('Property'), queryset=DescriptiveProperty.objects.all())
    q = forms.CharField(required=False, label=(''), widget=forms.TextInput(attrs={'type': 'search'}))
        
    def no_query_found(self):
        return self.searchqueryset.all()
        
    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(PropertySelectorSearchForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        return sqs