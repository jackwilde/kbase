from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'kbase/dashboard.html'
    login_url = reverse_lazy('sign-in')