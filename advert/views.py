from django.shortcuts import render
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template


def index(request):
    return render(request, 'index.html')


def other_page(request, page):
    try:
        template = get_template(f'{page}.html')
    except TemplateDoesNotExist:
        raise Http404

    return render(request, template)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')
