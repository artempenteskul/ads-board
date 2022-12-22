from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature

from django.contrib.auth.views import (
    LoginView, LogoutView,
    PasswordChangeView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


from advert.models import Advert

from .models import AdvUser
from .forms import ChangeUserInfoForm, RegisterUserForm
from .utils import signer


class UserLoginView(LoginView):
    template_name = 'user/login.html'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'user/logout.html'


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView, SuccessMessageMixin):
    template_name = 'password/password_change.html'
    success_url = reverse_lazy('advert:profile')
    success_message = 'Password was changed'


class UserPasswordResetView(PasswordResetView):
    template_name = 'password/reset_password.html'
    subject_template_name = 'email/reset_password_subject.txt'
    email_template_name = 'email/reset_password_body.txt'
    success_url = reverse_lazy('advert:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/reset_password_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView, SuccessMessageMixin):
    template_name = 'password/reset_password_confirm.html'
    post_reset_login = True
    success_url = reverse_lazy('advert:index')
    success_message = 'Password was changed'


class UserChangeInfoView(LoginRequiredMixin, UpdateView, SuccessMessageMixin):
    model = AdvUser
    template_name = 'user/change_user_info.html'
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


class UserRegisterView(CreateView):
    model = AdvUser
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('advert:register_done')


class UserRegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'user/delete_user.html'
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


@login_required
def profile(request):
    ads = Advert.objects.filter(author=request.user.pk)
    return render(request, 'user/profile.html', {'ads': ads})


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'registration/bad_signature.html')

    user = get_object_or_404(AdvUser, username=username)

    if user.is_activated:
        template = 'user_is_activated.html'
    else:
        template = 'activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()

    return render(request, template)
