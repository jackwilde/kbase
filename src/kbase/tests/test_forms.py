from django.test import TestCase
from authentication.models import User
from kbase.forms import ArticleForm
from django.utils.crypto import get_random_string

TEST_USER_PASSWORD = get_random_string(length=24)

class ArticleFormTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='existinguser@example.com',
            first_name='Existing',
            last_name='User',
            password=TEST_USER_PASSWORD
        )

    def test_form_valid(self):
        # Test form is valid with correct data
        form_data = {
            'title': 'New Article',
            'content': 'This is a new article.',
            'groups_with_view': [1],
            'groups_with_edit': [1],
        }
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Also test without groups
        form_data = {
            'title': 'New Article',
            'content': 'This is a new article.',
            'groups_with_view': [],
            'groups_with_edit': [],
        }
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_empty_title(self):
        # Test form is invalid with empty title
        form_data = {
            'title': '',
            'content': 'This is a new article.',
            'groups_with_view': [],
            'groups_with_edit': [],
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['Article title is required'])

    def test_form_invalid_title(self):
        # Test form is invalid with invalid title
        form_data = {
            'title': 'This is A [NEW] <Art!cle>',
            'content': 'This is a new article.',
            'groups_with_view': [],
            'groups_with_edit': [],
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'], ['Title can only contain letters, numbers, spaces, hyphens, and underscores.'])

    def test_form_invalid_adding_non_existent_groups(self):
        # Users should not be able to do this via the interface without modification anyway

        # Test adding group id that doesn't exist to view
        form_data = {
            'title': '',
            'content': 'This is a new article.',
            'groups_with_view': [2],
            'groups_with_edit': [],
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('groups_with_view', form.errors)
        self.assertEqual(form.errors['groups_with_view'], ['Select a valid choice. 2 is not one of the available choices.'])

        # Test adding group id that doesn't exist to edit
        form_data = {
            'title': '',
            'content': 'This is a new article.',
            'groups_with_view': [],
            'groups_with_edit': [2],
        }
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('groups_with_edit', form.errors)
        self.assertEqual(form.errors['groups_with_edit'], ['Select a valid choice. 2 is not one of the available choices.'])