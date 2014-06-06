""" Views for the base application """

from django.shortcuts import render
from base.models import Media

def home(request):
    """ Default view for the root """
	
    """ Load featured images """
    featured_imgs = Media.objects.filter(featured = True)
    context = {'featured_imgs': featured_imgs}
	
    return render(request, 'base/home.html', context)
