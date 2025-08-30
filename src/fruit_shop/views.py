from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
)
from django.contrib.auth import login
from django.contrib import messages

from .forms import AuthenticationForm


class PageView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)

        context.update({
            'auth_form': AuthenticationForm(),
        })

        return context

class LoginView(DjangoLoginView):
    template_name = 'main.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, 'User logged in successfully.')
        return redirect(reverse_lazy('app:page'))

    def form_invalid(self, form):
        messages.error(self.request, 'Authorization failed.')
        return redirect(reverse_lazy('app:page'))


class LogoutView(DjangoLogoutView):
    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'User logged out successfully.')
        return super(LogoutView, self).post(request, *args, **kwargs)
