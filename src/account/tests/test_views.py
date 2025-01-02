from django.test import TestCase
from django.urls import reverse

from authentication.models import User


class UnauthenticatedUserViewsTestCase(TestCase):
    def test_my_account_redirect(self):
        # Check that unauthenticated users get sent to sign-in page
        response = self.client.get(reverse('my-account'))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('my-account')}')

    def test_change_password_redirect(self):
        # Check that unauthenticated users get sent to sign-in page
        response = self.client.get(reverse('change-password'))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('change-password')}')


class AuthenticatedUserViewsTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123'
        )
        self.user.is_verified = True
        self.user.save()
        # Log user in
        self.client.login(email='testuser@example.com', password='djangopassword123')

    def test_my_account_view(self):
        # Check that authenticated users get the correct template and data
        response = self.client.get(reverse('my-account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/account.html')
        self.assertEqual(response.context['user'], self.user)

    def test_change_password_view(self):
        # Check that authenticated users get the correct template and data
        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/change-password.html')
        self.assertEqual(response.context['user'], self.user)

    def test_my_account_view_post(self):
        # Check that view accepts post with valid data and redirects
        data= {
            'first_name': 'New',
            'last_name': 'Name',
            'email': 'newname@example.com',
        }
        response = self.client.post(reverse('my-account'), data)
        # Check that view accepts post
        self.assertRedirects(response, reverse('dashboard'))

    def test_change_password_view_post(self):
        # Check that view accepts post with valid data and redirects
        data= {
            'old_password': 'djangopassword123',
            'new_password1': 'newdjangopassword123',
            'new_password2': 'newdjangopassword123',
        }
        response = self.client.post(reverse('change-password'), data)
        # Check that view accepts post
        self.assertRedirects(response, reverse('my-account'))
