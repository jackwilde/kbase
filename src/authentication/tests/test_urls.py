from django.test import TestCase
from django.urls import reverse

class UrlsTestCase(TestCase):
    def test_redirect_root_url(self):
        # Test / redirects to sign-in
        response = self.client.get('/')
        self.assertRedirects(response, f'{reverse('sign-in')}?next=/')

    def test_sign_in_url(self):
        # Test sign-in URL resolves and returns correct response
        response = self.client.get(reverse('sign-in'))
        self.assertEqual(response.status_code, 200)

    def test_sign_up_url(self):
        # Test sign-up URL resolves and returns correct response
        response = self.client.get(reverse('sign-up'))
        self.assertEqual(response.status_code, 200)

    def test_sign_out_url(self):
        # Test sign-out URL redirects
        response = self.client.post(reverse('sign-out'))
        self.assertEqual(response.status_code, 302)
