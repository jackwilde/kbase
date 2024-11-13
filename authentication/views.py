from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from .forms import SignUpForm, SignInForm


# Create your views here.
@method_decorator(login_not_required, name='dispatch')
class SignInView(LoginView):
    template_name = 'authentication/sign-in.html'
    next_page = reverse_lazy('dashboard')
    form_class = SignInForm


class SignOutView(LogoutView):
    next_page = reverse_lazy('sign-in')


@method_decorator(login_not_required, name='dispatch')
class SignUpView(FormView):
    template_name = 'authentication/sign-up.html'
    form_class = SignUpForm
    success_url = reverse_lazy(viewname='sign-in')
    next_page = reverse_lazy(viewname='dashboard')

    def form_valid(self, form):
        user = form.save()
        # Make the first registered user an admin
        if user.pk == 1:
            user.is_admin = True
            user.save()

        return super().form_valid(form)