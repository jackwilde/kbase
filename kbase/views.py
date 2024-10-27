from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView


# Create your views here.
class DashboardView(TemplateView):
    template_name = 'kbase/dashboard.html'
    login_url = reverse_lazy('sign-in')


class NewArticleView(FormView):
    pass