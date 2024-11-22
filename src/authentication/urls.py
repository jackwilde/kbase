from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('dashboard'), permanent=True)),
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),
]