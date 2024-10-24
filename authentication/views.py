from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import SignupForm


# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/index.html'
    login_url = reverse_lazy('login')


class AppLoginView(LoginView):
    template_name = 'authentication/login.html'
    next_page = reverse_lazy('home')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.next_page)
        return super().dispatch(request, *args, **kwargs)


class AppLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class SignupView(FormView):
    template_name = 'authentication/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy(viewname='login')
    next_page = reverse_lazy(viewname='home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.next_page)
        return super().dispatch(request, *args, **kwargs)
