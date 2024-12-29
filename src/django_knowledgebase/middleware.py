from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class VerifiedUserMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Do nothing to verified authenticated users
        if request.user.is_authenticated and request.user.is_verified:
            return None

        # Do nothing to unauthenticated users
        if not request.user.is_authenticated:
            return None

        # Sign out and redirect unverified users who try and sign in
        if request.user.is_authenticated and not request.user.is_verified:
            logout(request)
            messages.warning(request, 'Your account is not verified and has been signed out. '
                                      'Check your email or request a new verification link.')
            return redirect(reverse('re-verify'))

        return None