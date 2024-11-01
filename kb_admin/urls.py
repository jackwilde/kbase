from django.urls import path

from . import views

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='admin-dashboard'),
]