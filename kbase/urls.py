from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('new/', views.NewArticleView.as_view(), name='new-article'),
    path('<slug:slug>/', views.ArticleView.as_view(), name='article'),
    path('<slug:slug>/edit/', views.EditArticleView.as_view(), name='edit-article'),
]