""" Views for the base application """

from django.shortcuts import render
from base.models import GlobalVars
from base.utils import load_globals

def home(request):
    """ Default view for the root """
	
    """ Load global variables at add to context """
    context = load_globals()
	
    return render(request, 'base/home.html', context)
