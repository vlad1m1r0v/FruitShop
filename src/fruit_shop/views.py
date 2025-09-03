from django.template.loader import render_to_string
from django.utils.timezone import now
from django.http.response import (
    HttpResponse,
    JsonResponse
)
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import (
    TemplateView,
    FormView,
    View
)
from django.contrib.auth.views import (
    LogoutView as DjangoLogoutView,
    LoginView as DjangoLoginView,
)
from django.contrib.auth import login
from django.contrib import messages
from django.db.models.query import Prefetch

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from .models import (
    Declaration,
    Balance,
    Fruit,
    Trade
)

from .forms import (
    AuthenticationForm,
    DeclarationForm
)

from .tasks import financial_audit


class PageView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)

        today_count = Declaration.objects.filter(
            timestamp__date=now().date()
        ).count()

        balance = Balance.objects.first()

        last_trades_qs = (
            Trade.objects
            .filter(status=Trade.Status.SUCCESS)
            .order_by("fruit_id", "-timestamp")
        )

        fruits = (
            Fruit.objects
            .prefetch_related(
                Prefetch(
                    "trade_set",
                    queryset=last_trades_qs,
                    to_attr="successful_trades"
                )
            )
            .order_by("id")
        )

        context.update({
            'auth_form': AuthenticationForm(),
            'declaration_form': DeclarationForm(),
            'declarations_count': today_count,
            'balance': balance.value,
            'fruits': fruits
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
    next_page = reverse_lazy('app:page')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'User logged out successfully.')
        return super(LogoutView, self).post(request, *args, **kwargs)


class AuditView(View):
    @staticmethod
    def post(*args, **kwargs):
        financial_audit.delay()
        return HttpResponse(status=204)


class DeclarationView(FormView):
    form_class = DeclarationForm

    def form_valid(self, form):
        form.save()

        today_count = Declaration.objects.filter(
            timestamp__date=now().date()
        ).count()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'declaration',
            {
                'type': 'declaration_upload',
                'today_count': today_count
            }
        )

        return HttpResponse(status=204)

    def form_invalid(self, form):
        return JsonResponse(
            status=400,
            data={'error': 'Invalid file format: expected xlsx or xls.'}
        )


class WarehouseView(View):
    @staticmethod
    def get(*args, **kwargs):
        last_trades_qs = (
            Trade.objects
            .filter(status=Trade.Status.SUCCESS)
            .order_by("fruit_id", "-timestamp")
        )

        fruits = (
            Fruit.objects
            .prefetch_related(
                Prefetch(
                    "trade_set",
                    queryset=last_trades_qs,
                    to_attr="successful_trades"
                )
            )
            .order_by("id")
        )

        return HttpResponse(
            render_to_string(
                template_name="partials/fruits.html",
                context={'fruits': fruits}
            )
        )
