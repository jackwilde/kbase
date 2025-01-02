from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from authentication.models import User

TEST_USER_PASSWORD = get_random_string(length=24)

class UnauthenticatedUserViewsTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
        email='testuser@example.com',
        first_name='Test',
        last_name='User',
        password=TEST_USER_PASSWORD
        )
        self.user.is_verified = True
        self.user.save()

    def test_get_sign_in_view(self):
        # Test sign in view returns the correct template successfully
        response = self.client.get(reverse('sign-in'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/sign-in.html')

    def test_get_sign_up_view(self):
        # Test sign in view returns the correct template successfully
        response = self.client.get(reverse('sign-up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/sign-up.html')

    def test_post_sign_in_view(self):
        # Test sign in view allows existing user to sign in
        response = self.client.post(reverse('sign-in'), {
            'username': 'testuser@example.com',
            'password': TEST_USER_PASSWORD
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_sign_in_view_incorrect(self):
        # Test sign in view fails to log in with incorrect details
        response = self.client.post(reverse('sign-in'), {
            'username': 'incorrect@example.com',
            'password': get_random_string(length=20)
        })
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertTemplateUsed(response, 'authentication/sign-in.html')

    def test_post_sign_up_view(self):
        # Test sign up view accepts post request
        response = self.client.post(reverse('sign-up'), {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'djangopassword123',
            'password2': 'djangopassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/sign-up.html')

    def test_get_verify_view(self):
        # Test sign in view returns the correct template successfully
        response = self.client.get(reverse('verify-email', kwargs={'token': get_random_string(32)}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('sign-in'))

    def test_get_re_verify_view(self):
        # Test sign in view returns the correct template successfully
        response = self.client.get(reverse('re-verify'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('re-verify')}')


class UnverifiedUserViewsTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password=TEST_USER_PASSWORD
        )
        # Log user in
        self.client.login(email='testuser@example.com', password=TEST_USER_PASSWORD)

    def test_get_sign_in_view(self):
        # Test sign in redirects to re-verify
        response = self.client.get(reverse('sign-in'))
        self.assertRedirects(response, reverse('re-verify'), status_code=302)

    def test_get_sign_up_view(self):
        # Test sign up redirects to re-verify
        response = self.client.get(reverse('sign-up'))
        self.assertRedirects(response, reverse('re-verify'), status_code=302)

    def test_get_verify_view(self):
        # Test sign in view returns the correct template successfully
        response = self.client.get(reverse('verify-email', kwargs={'token': get_random_string(32)}))
        self.assertRedirects(response, reverse('re-verify'), status_code=302)

    def test_get_re_verify_view(self):
        # Test sign in view returns the correct template successfully
        response = self.client.get(reverse('re-verify'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/re-verify.html')

    def test_sign_out_view(self):
        # Test unverified users can still sign out

        # Test user is authenticated with 200 response from re-verify
        response = self.client.get(reverse('re-verify'))
        self.assertEqual(response.status_code, 200)

        # Test user logout. Should return 302 and redirect to sign-in
        response = self.client.post(reverse('sign-out'))
        self.assertRedirects(response, reverse('sign-in'))

        # Test user is unauthenticated if / redirects to sign-in
        response = self.client.get('/')
        self.assertRedirects(response, f'{reverse('sign-in')}?next=/')


class AuthenticatedViewsTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
        email='testuser@example.com',
        first_name='Test',
        last_name='User',
        password=TEST_USER_PASSWORD
        )
        self.user.is_verified = True
        self.user.save()
        # Log user in
        self.client.login(email='testuser@example.com', password=TEST_USER_PASSWORD)

    def test_redirect_root_view(self):
        # Test / redirects to dashboard
        response = self.client.get('/')
        self.assertRedirects(response, reverse('dashboard'), status_code=301)

    def test_sign_in_view(self):
        # Test sign-in URL redirects to dashboard
        response = self.client.get(reverse('sign-in'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_sign_up_view(self):
        # Test sign-up URL redirects to dashboard
        response = self.client.get(reverse('sign-up'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_sign_out_view(self):
        # Test user is authenticated with 200 response from dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        # Test user logout. Should return 302 and redirect to sign-in
        response = self.client.post(reverse('sign-out'))
        self.assertRedirects(response, reverse('sign-in'))

        # Test user is unauthenticated if / redirects to sign-in
        response = self.client.get('/')
        self.assertRedirects(response, f'{reverse('sign-in')}?next=/')