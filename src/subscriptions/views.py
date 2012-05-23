# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

def subscribe(request):
    #from django.conf import settings
    #context = RequestContext(request)
    #return render_to_response('index.html', context)
    return HttpResponse()


def success(request, pk):
    #from django.conf import settings
   # context = RequestContext(request, pk)
    #return render_to_response('index.html', context, pk)
    return HttpResponse(pk)