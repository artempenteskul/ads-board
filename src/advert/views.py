from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import (
    PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth import logout
from django.contrib import messages
from django.core.signing import BadSignature


from .models import CustomUser
from .forms import ChangeUserForm, RegisterUserForm
from .utilities import signer


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
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(PasswordChangeView, LoginRequiredMixin, SuccessMessageMixin):
    template_name = 'advert/password_change.html'
    success_url = reverse_lazy('advert:profile')
    success_message = 'Your password was successfully changed'


class UserPasswordResetView(PasswordResetView, SuccessMessageMixin):
    template_name = 'advert/password_reset.html'
    subject_template_name = 'email/password_reset_subject.txt'
    email_template_name = 'email/password_reset_body.txt'
    success_url = reverse_lazy('advert:password-reset-done')


class UserPasswordDoneResetView(PasswordResetDoneView):
    template_name = 'advert/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'advert/password_reset_confirm.html'
    post_reset_login = True
    success_url = reverse_lazy('advert:password-complete-reset')


class UserPasswordCompleteResetView(PasswordResetCompleteView):
    template_name = 'advert/password_reset_complete.html'


class RegisterUserView(CreateView):
    model = CustomUser
    template_name = 'advert/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('advert:register-done')


class RegisterUserDoneView(TemplateView):
    template_name = 'advert/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'advert/activation_done.html')
    user = get_object_or_404(CustomUser, username=username)
    if user.is_activated:
        template = 'advert/user_is_activated.html'
    else:
        template = 'advert/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'advert/delete_user.html'
    success_url = reverse_lazy('advert:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super(DeleteUserView, self).setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User was successfully deleted')
        return super(DeleteUserView, self).post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)



