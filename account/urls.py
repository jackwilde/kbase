from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccountView.as_view(), name='my-account'),
    path('password/', views.ResetPasswordView.as_view(), name='change-password'),
]