from django.views.generic import TemplateView


# Create your views here.
class AccountView(TemplateView):
    template_name = 'account/account.html'
