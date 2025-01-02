from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.conf import settings
from django.views.generic.base import View
from django.contrib import messages
from .forms import SignUpForm, SignInForm
from .utils import EmailVerificationTokenGenerator, InvalidTokenError, send_verification_email, EmailRequestTooSoonError
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
            if not request.user.is_verified:
                messages.warning(request, 'You need to verify you account before signing in. '
                                          'Please check your email or request a new verification link.')
                return redirect(reverse_lazy('re-verify'))
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

        token = EmailVerificationTokenGenerator().make_token(user)
        verification_link = f"{settings.SITE_URL}/verify/{token}/"
        send_verification_email(user, verification_link)
        messages.success(self.request, 'Thank you for signing up! Please check your email for verification link.')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_not_required, name='dispatch')
class VerifyEmailView(View):
    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated and already verified
        if request.user.is_authenticated and request.user.is_verified:
            messages.warning(request, 'Account is already verified.')
            return redirect(reverse_lazy('dashboard'))

        # Extract token from the URL
        token = kwargs.get('token')
        token_generator = EmailVerificationTokenGenerator()

        try:
            # Decode the token
            decoded_data = token_generator.decode_token(token)
            email = decoded_data["email"]
            token = decoded_data["token"]

            # Get the user details
            user = User.objects.get(email=email)

            # If the user is already verified, redirect to the dashboard
            if user.is_verified:
                messages.warning(request, 'Account is already verified.')
                return redirect(reverse_lazy('dashboard'))

            # Check the real token
            if token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                messages.success(request, 'Your email has been successfully verified!')
                return redirect(reverse_lazy('sign-in'))

        except (InvalidTokenError, User.DoesNotExist):
            # If user is logged in send them to reverification page
            if self.request.user.is_authenticated:
                messages.warning(request, 'Verification link is invalid or expired. '
                                          'Please request a new verification link.')
                return redirect(reverse_lazy('re-verify'))
            # If user is not logged in send them to sign in
            else:
                messages.warning(request, 'Verification link is invalid or expired. '
                                          'Please sign in to request a new verification link.')
                return redirect(reverse_lazy('sign-in'))

        # Fallback error message for unexpected issues
        messages.warning(request, 'An unexpected error occurred. Please request a new verification link.')
        return redirect(reverse_lazy('sign-in'))


class ReVerifyEmailView(View):
    template_name = 'authentication/re-verify.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        if request.user.is_verified:
            return redirect(reverse_lazy('dashboard'))
        return render(request, 'authentication/re-verify.html')

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_verified:
            token = EmailVerificationTokenGenerator().make_token(user)
            verification_link = f"{settings.SITE_URL}/verify/{token}/"
            try:
                send_verification_email(user, verification_link)
                messages.success(request, 'Verification email has been sent.')
            except EmailRequestTooSoonError:
                messages.warning(self.request, 'A verification link has been sent been sent recently. '
                                             'Please check your emails or try again later.')
            return render(request, 'authentication/re-verify.html')
