from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


class AdsBoardLoginView(LoginView):
    template_name = 'login.html'


class AdsBoardLogoutView(LogoutView, LoginRequiredMixin):
    template_name = 'logout.html'


@login_required
def profile(request):
    return render(request, 'profile.html')


def other_page(request, page):
    try:
        template = get_template(f'{page}.html')
    except TemplateDoesNotExist:
        raise Http404

    return HttpResponse(template.render(request=request))

