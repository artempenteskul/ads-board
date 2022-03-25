from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist
from django.template.loader import get_template


def index(request):
    return render(request, 'advert/index.html')


def other_page(request, page):
    try:
        template = get_template('advert/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


@login_required
def profile(request):
    return render(request, 'advert/profile.html')


class AdvertLoginView(LoginView):
    template_name = 'advert/login.html'


class AdvertLogout(LogoutView, LoginRequiredMixin):
    template_name = 'advert/logout.html'
