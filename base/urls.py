"""urlconf for the base application"""

from django.conf.urls import url, patterns, include
from forms import AdvancedSearchForm
from haystack.views import SearchView, search_view_factory

urlpatterns = patterns('base.views',
    url(r'^$', 'home', name='home'),
    url(r'^map/', 'map', name='map'),
    url(r'^search/', search_view_factory(
        form_class = AdvancedSearchForm
    ), name='haystack_search'),
    # ex: /ur.iaas.upenn.edu/subject/5/
    url(r'^subject/(?P<subject_id>\d+)/$', 'subjectdetail', name='subjectdetail'),
    # ex: /ur.iaas.upenn.edu/personorg/5/
    url(r'^(?P<personorg_id>\d+)/$', 'personorgdetail', name='personorgdetail'),
    # ex: /ur.iaas.upenn.edu/media/5/
    url(r'^media/(?P<media_id>\d+)/$', 'mediadetail', name='mediadetail'),
    url(r'^search_help/', 'search_help', name='search_help'),
)
