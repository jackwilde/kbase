from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
]