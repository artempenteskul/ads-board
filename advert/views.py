from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature
from django.contrib import messages

from .models import AdvUser
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utils import signer


def index(request):
    return render(request, 'index.html')


class AdsBoardLoginView(LoginView):
    template_name = 'login.html'


class AdsBoardLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'


class AdsBoardPasswordChangeView(LoginRequiredMixin, PasswordChangeView, SuccessMessageMixin):
    template_name = 'password_change.html'
    success_url = reverse_lazy('advert:profile')
    success_message = 'Password was changed'


class ChangeUserInfoView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
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


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('advert:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('advert:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User was deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'bad_signature.html')

    user = get_object_or_404(AdvUser, username=username)

    if user.is_activated:
        template = 'user_is_activated.html'
    else:
        template = 'activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()

    return render(request, template)


@login_required
def profile(request):
    return render(request, 'profile.html')


def other_page(request, page):
    try:
        template = get_template(f'{page}.html')
    except TemplateDoesNotExist:
        raise Http404

    return HttpResponse(template.render(request=request))

