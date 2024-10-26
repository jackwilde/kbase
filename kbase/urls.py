from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('dashboard'))),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]