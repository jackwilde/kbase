from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView
from authentication.models import User


# Create your views here.
class AccountView(UpdateView):
    template_name = 'account/account.html'
    model = User
    fields = ["first_name", "last_name", "email"]
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        return self.request.user


class ResetPasswordView(TemplateView):
    template_name = 'account/reset-password.html'
