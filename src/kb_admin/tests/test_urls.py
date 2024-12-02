from django.test import TestCase
from django.urls import reverse

from authentication.models import User, Group


class UrlsTestCase(TestCase):
    # All these tests should redirect unauthenticated user to the sign-in page
    def test_admin_dashboard_url(self):
        response = self.client.get(reverse('admin-dashboard'))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('admin-dashboard')}')

    def test_all_users_url(self):
        response = self.client.get(reverse('all-users'))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('all-users')}')

    def test_user_detail_url(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': 1}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('user-detail', kwargs={'pk': 1})}')

    def test_user_delete_url(self):
        response = self.client.get(reverse('user-delete', kwargs={'pk': 1}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('user-delete', kwargs={'pk': 1})}')

    def test_set_permissions_url(self):
        response = self.client.get(reverse('set-permissions', kwargs={'pk': 1}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('set-permissions', kwargs={'pk': 1})}')

    def test_all_groups_url(self):
        response = self.client.get(reverse('all-groups'))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('all-groups')}')

    def test_create_group_url(self):
        response = self.client.get(reverse('create-group'))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('create-group')}')

    def test_group_detail_url(self):
        response = self.client.get(reverse('group-detail', kwargs={'pk': 1}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('group-detail', kwargs={'pk': 1})}')

    def test_group_edit_url(self):
        response = self.client.get(reverse('group-edit', kwargs={'pk': 1}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('group-edit', kwargs={'pk': 1})}')

    def test_group_delete_url(self):
        response = self.client.get(reverse('group-delete', kwargs={'pk': 1}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('group-delete', kwargs={'pk': 1})}')


class AuthenticatedUrlsTestCase(TestCase):
    # These test authenticated non admin user. They should all redirect to standard dashboard
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123'
        )
        self.user2 = User.objects.create_user(
            email='seconduser@example.com',
            first_name='Second',
            last_name='User',
            password='djangopassword123'
        )

        # Create test group
        self.group = Group.objects.create(name='testgroup')

        # Log user in
        self.client.login(email='testuser@example.com', password='djangopassword123')

    def test_admin_dashboard_url(self):
        response = self.client.get(reverse('admin-dashboard'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_all_users_url(self):
        response = self.client.get(reverse('all-users'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_user_detail_url(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user2.pk}))
        self.assertRedirects(response, reverse('dashboard'))

    def test_user_delete_url(self):
        # Test against another user as there is protection in place to stop user deleting themselves
        response = self.client.post(reverse('user-delete', kwargs={'pk': self.user2.pk}))
        self.assertRedirects(response, reverse('dashboard'))

    def test_set_permissions_url(self):
        # Test against another user as there is protection in place to stop user changing their permissions
        response = self.client.post(reverse('set-permissions', kwargs={'pk': self.user2.pk}))
        self.assertRedirects(response, reverse('dashboard'))

    def test_all_groups_url(self):
        response = self.client.get(reverse('all-groups'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_create_group_url(self):
        response = self.client.get(reverse('create-group'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_group_detail_url(self):
        response = self.client.get(reverse('group-detail', kwargs={'pk': self.group.pk}))
        self.assertRedirects(response, reverse('dashboard'))

    def test_group_edit_url(self):
        # Don't test against group id 1 because it's protected
        response = self.client.get(reverse('group-edit', kwargs={'pk': self.group.pk}))
        self.assertRedirects(response, reverse('dashboard'))

    def test_group_delete_url(self):
        response = self.client.post(reverse('group-delete', kwargs={'pk': self.group.pk}))
        self.assertRedirects(response, reverse('dashboard'))