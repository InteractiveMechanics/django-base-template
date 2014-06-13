"""urlconf for the base application"""

from django.conf.urls import url, patterns, include
from forms import PropertySelectorSearchForm
from haystack.views import SearchView, search_view_factory

urlpatterns = patterns('base.views',
    url(r'^$', 'home', name='home'),
    url(r'^map/', 'map', name='map'),
    url(r'^search/', search_view_factory(
        form_class = PropertySelectorSearchForm
    ), name='haystack_search'),
)
