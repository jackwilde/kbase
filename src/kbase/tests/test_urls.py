from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from authentication.models import User

# Generate a random user password for test accounts
TEST_USER_PASSWORD = get_random_string(length=24)

class UrlsTestCase(TestCase):
    # All these tests should redirect unauthenticated user to the sign-in page
    def test_dashboard_url(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('dashboard')}')

    def test_new_article_url(self):
        response = self.client.get(reverse('new-article'))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('new-article')}')

    def test_article_url(self):
        response = self.client.get(reverse('article', kwargs={'slug': 'test'}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('article', kwargs={'slug': 'test'})}')

    def test_edit_article_url(self):
        response = self.client.get(reverse('edit-article', kwargs={'slug': 'test'}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('edit-article', kwargs={'slug': 'test'})}')

    def test_delete_article_url(self):
        response = self.client.get(reverse('delete-article', kwargs={'slug': 'test'}))
        self.assertRedirects(response, f'{reverse('sign-in')}?next={reverse('delete-article', kwargs={'slug': 'test'})}')


class UnverifiedUserUrlsTestCase(TestCase):
    # All these tests should redirect unverified user to the re-verify page
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password=TEST_USER_PASSWORD,
        )

        # Log user in
        self.client.login(email='testuser@example.com', password=TEST_USER_PASSWORD)

    def test_dashboard_url(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('re-verify'))

    def test_new_article_url(self):
        response = self.client.get(reverse('new-article'))
        self.assertRedirects(response, reverse('re-verify'))

    def test_article_url(self):
        response = self.client.get(reverse('article', kwargs={'slug': 'test'}))
        self.assertRedirects(response, reverse('re-verify'))

    def test_edit_article_url(self):
        response = self.client.get(reverse('edit-article', kwargs={'slug': 'test'}))
        self.assertRedirects(response, reverse('re-verify'))

    def test_delete_article_url(self):
        response = self.client.get(reverse('delete-article', kwargs={'slug': 'test'}))
        self.assertRedirects(response, reverse('re-verify'))



