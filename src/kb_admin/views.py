from django.core.exceptions import ValidationError, PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, View, CreateView, UpdateView

from .forms import GroupForm
from .mixins import AdminRequiredMixin
from kbase.models import Article
from authentication.models import User, Group
from django.contrib import messages


# Create your views here.
class DashboardAdminView(AdminRequiredMixin, TemplateView):
    template_name = 'kb_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        # Get the total number of articles
        total_articles = Article.objects.count()
        total_users = User.objects.count()
        total_groups = Group.objects.count()

        context = super().get_context_data(**kwargs)
        context['total_articles'] = total_articles
        context['total_users'] = total_users
        context['total_groups'] = total_groups

        return context


class UsersAdminView(AdminRequiredMixin, ListView):
    template_name = 'kb_admin/users.html'
    model = User
    context_object_name = 'users'


class UserDetailsAdminView(AdminRequiredMixin, DetailView):
    template_name = 'kb_admin/user-detail.html'
    model = User
    context_object_name = 'user'


class UserDeleteAdminView(AdminRequiredMixin, DeleteView):
    model = User
    context_object_name = 'user'
    success_url = reverse_lazy('all-users')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        # Prevent self-deletion
        if user == self.request.user:
            messages.error(self.request, "You cannot delete yourself.")
            # Redirect back to the user detail page
            return redirect(reverse_lazy('user-detail', kwargs={'pk': user.pk}))

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "User deleted successfully.")
        return super().delete(request, *args, **kwargs)


class UserSetPermissionsAdminView(AdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        # Prevent user removing or adding admin permissions to themselves
        if request.user == user:
            messages.error(self.request, "You cannot toggle admin for yourself.")
        else:
            user.is_admin = not user.is_admin
            user.save()
            if user.is_admin:
                messages.success(request, f"{user.username} is now an admin.")
            else:
                messages.success(request, f"{user.username} is no longer an admin.")

        return redirect(reverse_lazy('user-detail', kwargs={'pk': user.pk}))


class GroupsAdminView(AdminRequiredMixin, ListView):
    template_name = 'kb_admin/groups.html'
    model = Group
    context_object_name = 'groups'


class GroupDetailsAdminView(AdminRequiredMixin, DetailView):
    template_name = 'kb_admin/group-detail.html'
    model = Group
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.get_object()
        if group.pk == 1:
            context['protected_group'] = True
        return context


class CreateGroupAdminView(AdminRequiredMixin, CreateView):
    template_name = 'kb_admin/group-new-edit.html'
    model = Group
    form_class = GroupForm

    def get_success_url(self):
        return reverse_lazy(viewname='group-detail', kwargs={'pk': self.object.pk})


class EditGroupAdminView(AdminRequiredMixin, UpdateView):
    template_name = 'kb_admin/group-new-edit.html'
    model = Group
    form_class = GroupForm
    object_name = 'group'

    def get_success_url(self):
        return reverse_lazy(viewname='group-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit_mode'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        if group.pk == 1:
            raise PermissionDenied('You cannot edit the "All Users" group.')
        return super().dispatch(request, *args, **kwargs)


class GroupDeleteAdminView(AdminRequiredMixin, DeleteView):
    model = Group
    context_object_name = 'group'
    success_url = reverse_lazy('all-groups')

    def dispatch(self, request, *args, **kwargs):
        group = self.get_object()
        if group.pk == 1:
            raise PermissionDenied('You cannot edit the "All Users" group.')
        return super().dispatch(request, *args, **kwargs)