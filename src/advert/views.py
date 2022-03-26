from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


from .models import CustomUser
from .forms import ChangeUserForm


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


class ChangeUserInfoView(UpdateView, SuccessMessageMixin, LoginRequiredMixin):
    model = CustomUser
    template_name = 'advert/change_user_info.html'
    form_class = ChangeUserForm
    success_url = reverse_lazy('advert:profile')
    success_message = 'Your info was successfully changed'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super(ChangeUserInfoView, self).setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

