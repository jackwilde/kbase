from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

class VerifiedUserMiddleware(MiddlewareMixin):
    """
    Custom middleware to redirect unverified users when they log in.
    This will prevent them from accessing anything inside the application until they are verified.
    """
    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Views that are allowed without verification
        self.allowed_views = (
            'verify-email',
            'sign-out',
            're-verify'
        )

    def process_view(self, request):
        """
        Checks if the user is verified and redirects them to the re-verification page if they are not.
        """
        # Do nothing to unauthenticated users
        if not request.user.is_authenticated:
            return None
        # Do nothing to verified users
        elif request.user.is_verified:
            return None
        # Redirect unverified users to the reverify page
        elif resolve(request.path).view_name not in self.allowed_views:
            messages.warning(request, 'Your account is not verified. '
                                      'Check your email or request a new verification link.')
            return redirect(reverse('re-verify'))
