from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import AdvUser
from .forms import ChangeUserInfoForm


def index(request):
    return render(request, 'index.html')


class AdsBoardLoginView(LoginView):
    template_name = 'login.html'


class AdsBoardLogoutView(LogoutView, LoginRequiredMixin):
    template_name = 'logout.html'


class ChangeUserInfoView(UpdateView, LoginRequiredMixin, SuccessMessageMixin):
    model = AdvUser
    template_name = 'change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('advert:profile')
    success_message = 'User info was changed'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


@login_required
def profile(request):
    return render(request, 'profile.html')


def other_page(request, page):
    try:
        template = get_template(f'{page}.html')
    except TemplateDoesNotExist:
        raise Http404

    return HttpResponse(template.render(request=request))

