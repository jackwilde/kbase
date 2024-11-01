from django.views.generic import TemplateView
from .mixins import AdminRequiredMixin


# Create your views here.
class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'kb_admin/dashboard.html'
