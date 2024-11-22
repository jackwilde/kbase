from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardAdminView.as_view(), name='admin-dashboard'),
    path('user/', views.UsersAdminView.as_view(), name='all-users'),
    path('user/<int:pk>', views.UserDetailsAdminView.as_view(), name='user-detail'),
    path('user/<int:pk>/delete/', views.UserDeleteAdminView.as_view(), name='user-delete'),
    path('user/<int:pk>/set-permissions/', views.UserSetPermissionsAdminView.as_view(), name='set-permissions'),
    path('group/', views.GroupsAdminView.as_view(), name='all-groups'),
    path('group/create/', views.CreateGroupAdminView.as_view(), name='create-group'),
    path('group/<int:pk>', views.GroupDetailsAdminView.as_view(), name='group-detail'),
    path('group/<int:pk>/edit/', views.EditGroupAdminView.as_view(), name='group-edit'),
    path('group/<int:pk>/delete/', views.GroupDeleteAdminView.as_view(), name='group-delete'),
]
