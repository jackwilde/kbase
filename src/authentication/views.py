from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from .forms import SignUpForm, SignInForm
from .models import User

# Decorator required because by default ALL views require login
@method_decorator(login_not_required, name='dispatch')
class SignInView(LoginView):
    template_name = 'authentication/sign-in.html'
    form_class = SignInForm
    next_page = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        return super().dispatch(request, *args, **kwargs)


class SignOutView(LogoutView):
    next_page = reverse_lazy('sign-in')


# Decorator required because by default ALL views require login
@method_decorator(login_not_required, name='dispatch')
class SignUpView(FormView):
    template_name = 'authentication/sign-up.html'
    form_class = SignUpForm
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'A user with this email already exists.')
            return self.form_invalid(form)

        user = form.save()
        # Make the first registered user an admin
        if user.pk == 1:
            user.is_admin = True
            user.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        return super().dispatch(request, *args, **kwargs)
