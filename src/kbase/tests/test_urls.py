from django.test import TestCase
from django.urls import reverse


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



