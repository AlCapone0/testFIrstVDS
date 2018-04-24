from django.shortcuts import render
from django.http import HttpResponse
from .newdict import sumspares, needtobuy


def table_list(request):
    context = sumspares
    return render (request, 'table_list.html', {'context':context})


def json_needtobuy(request):
    x = str(needtobuy())
    return HttpResponse(x)
