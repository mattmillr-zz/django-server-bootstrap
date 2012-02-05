from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response('simple_blog/index.html', {}, RequestContext(request))