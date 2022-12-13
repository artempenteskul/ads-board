from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView


def index(request):
    return render(request, 'index.html')


def other_page(request, page):
    try:
        template = get_template(f'{page}.html')
    except TemplateDoesNotExist:
        raise Http404

    return HttpResponse(template.render(request=request))


class AdsBoardLoginView(LoginView):
    template_name = 'login.html'
