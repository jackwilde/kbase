from django.views.generic import TemplateView


# Create your views here.
class AdminDashboardView(TemplateView):
    template_name = 'kb_admin/dashboard.html'
