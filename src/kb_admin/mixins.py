from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class AdminRequiredMixin(LoginRequiredMixin):
    """
    Custom subclass of LoginRequiredMixin that checks that the user is admin
    """
    def dispatch(self, request, *args, **kwargs):
        # Return normal behaviour for unauthenticated users
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        # If user is authenticated, check that they are an admin. Redirect them to standard dashboard if not
        if not request.user.is_admin:
            return redirect(reverse_lazy('dashboard'))

        return super().dispatch(request, *args, **kwargs)