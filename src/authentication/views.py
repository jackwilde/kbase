from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.conf import settings
from django.views.generic.base import View
from django.contrib import messages
from .forms import SignUpForm, SignInForm, VerificationForm
from .utils import EmailVerificationTokenGenerator, InvalidTokenError
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
        send_mail(
            subject="Verify Your Email",
            message=f"Hi {user.first_name},\n\nPlease verify your email by clicking the link below:\n{verification_link}\n\nThank you!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
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
            messages.warning(request, 'Verification link is invalid or expired. Please request a new verification link.')
            return redirect(reverse_lazy('re-verify'))

        # Fallback error message for unexpected issues
        messages.warning(request, 'An unexpected error occurred. Please request a new verification link.')
        return redirect(reverse_lazy('re-verify'))


class ReVerifyEmailView(FormView):
    template_name = 'authentication/re-verify.html'
    form_class = VerificationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if not user.is_verified:
                token = EmailVerificationTokenGenerator().make_token(user)
                verification_link = f"{settings.SITE_URL}/verify/{token}/"
                send_mail(
                    subject="Verify Your Email",
                    message=f"Hi {user.first_name},\n\nPlease verify your email by clicking the link below:\n{verification_link}\n\nThank you!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )
        except User.DoesNotExist:
            pass
        messages.success(self.request, 'If the email is registered to an account a new verification link has been sent.')
        # Redirect to the success URL
        return super().form_valid(form)
