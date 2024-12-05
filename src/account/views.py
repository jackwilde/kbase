from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth.views import PasswordChangeView
from authentication.models import User


# Create your views here.
class AccountView(UpdateView):
    template_name = 'account/account.html'
    model = User
    fields = ["first_name", "last_name", "email"]
    success_url = reverse_lazy('dashboard')

    # Set object as the logged-in user
    def get_object(self, queryset=None):
        return self.request.user


class ResetPasswordView(PasswordChangeView):
    template_name = 'account/change-password.html'
    success_url = reverse_lazy('my-account')

    # Set object as the logged-in user
    def get_object(self, queryset=None):
        return self.request.user