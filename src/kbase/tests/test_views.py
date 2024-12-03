from django.test import TestCase
from django.urls import reverse

from authentication.models import User, Group
from kbase.models import Article
from django.utils.text import slugify


class BasicViewsTestCase(TestCase):
    # These test authenticated user basic access with valid inputs
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123',
        )

        # Log user in
        self.client.login(email='testuser@example.com', password='djangopassword123')

        # Create a test article
        self.test_article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            content='Test Content',
            created_by=self.user1,
        )
        self.test_article.save()

        self.test_group = Group.objects.get(id=1)

    def test_dashboard_view(self):
        # Test dashboard view returns the correct template successfully
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kbase/dashboard.html')

    def test_article_view(self):
        # Test article view returns the correct template successfully
        response = self.client.get(reverse('article', kwargs={'slug': self.test_article.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kbase/article.html')

    def test_new_article_view(self):
        # Test New Article view
        response = self.client.get(reverse('new-article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kbase/new-edit.html')
        self.assertNotIn('edit_mode', response.context)

        # Test POST request with valid data
        data = {
            'title': 'New Test Article',
            'content': 'Test content',
            'groups_with_view': [],
            'groups_with_edit': [],
        }
        response = self.client.post(reverse('new-article'), data=data)
        # Verify redirect URL
        self.assertRedirects(response, reverse('article', kwargs={'slug': slugify(data['title'])}))

        # Verify the article was created
        self.assertTrue(Article.objects.filter(title=data['title']).exists())

    def test_edit_article_view(self):
        # Test edit article view
        response = self.client.get(reverse('edit-article', kwargs={'slug': self.test_article.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kbase/new-edit.html')
        self.assertTrue(response.context['edit_mode'])

        test_group = self.test_group

        # Test POST request with valid data
        data = {
            'title': 'Updated Test Article',
            'content': 'New content',
            'groups_with_view': [test_group.id],
            'groups_with_edit': [test_group.id],
        }
        response = self.client.post(reverse('edit-article', kwargs={'slug': self.test_article.slug}), data=data)
        # Verify redirect URL
        self.assertRedirects(response, reverse('article', kwargs={'slug': slugify(data['title'])}))

        # Verify the article was created
        self.assertTrue(Article.objects.filter(title=data['title']).exists())

    def test_delete_article_view(self):
        # Test delete article view
        test_group = self.test_group
        response = self.client.post(reverse('delete-article', kwargs={'slug': self.test_article.slug}))
        # Verify redirect URL
        self.assertRedirects(response, reverse('dashboard'))

        # Verify the article was created
        self.assertFalse(Article.objects.filter(id=test_group.id).exists())


class AdvancedViewsTestCase(TestCase):
    # These test permissions on the kbase views
    def setUp(self):
        # Create some test users
        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123',
        )
        self.user2 = User.objects.create_user(
            email='testuser2@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123',
        )
        self.user3 = User.objects.create_user(
            email='testuser3@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123',
        )
        self.user3.is_admin = True
        self.user3.save()

        # Create some test groups
        self.test_group1 = Group.objects.create(
            name='Test Group 1',
        )
        self.test_group1.users.add(self.user1.id)
        self.test_group1.save()

        self.test_group2 = Group.objects.create(
            name='Test Group 2',
        )
        self.test_group2.users.add(self.user2.id)
        self.test_group2.save()

        # Create some test articles

        # This article should only be accessible/editable by user1 and admins (user3)
        self.test_article1 = Article.objects.create(
            title='Test Private Article',
            slug=slugify('Test Private Article'),
            content='Test Content',
            created_by=self.user1,
        )
        self.test_article1.save()

        # This article should be viewable by owner, group2 (user2) and admin (user3)
        self.test_article2 = Article.objects.create(
            title='Test Group 2 View Article',
            slug=slugify('Test Group 2 View Article'),
            content='Test Content',
            created_by=self.user1,
        )
        self.test_article2.groups_with_view.set([self.test_group2.id])
        self.test_article2.save()

        # This article should be viewable and editable by owner (user1), group2 (user2) and admin (user3)
        self.test_article3 = Article.objects.create(
            title='Test Group 2 Edit Article',
            slug=slugify('Test Group 2 Edit Article'),
            content='Test Content',
            created_by=self.user1,
        )
        self.test_article3.groups_with_view.set([self.test_group2.id])
        self.test_article3.groups_with_edit.set([self.test_group2.id])
        self.test_article3.save()

        # Should behave same as above despite not explicitly setting group2 view
        self.test_article4 = Article.objects.create(
            title='Test Group 2 Edit 2 Article',
            slug=slugify('Test Group 2 Edit 2 Article'),
            content='Test Content',
            created_by=self.user1,
        )
        self.test_article4.groups_with_edit.set([self.test_group2.id])
        self.test_article4.save()

        # This is private article owner by user2 for variation
        self.test_article5 = Article.objects.create(
            title='Test User 2 Article',
            slug=slugify('Test User 2 Article'),
            content='Test Content',
            created_by=self.user2,
        )
        self.test_article5.save()

    def test_dashboard_view_user_1(self):
        # Log in user1
        self.client.login(email=self.user1.email, password='djangopassword123')

        response = self.client.get(reverse('dashboard'))

        # Test how many articles are returned, user1 should see 4
        self.assertEqual(len(response.context['articles']), 4)
        # Also check user1 doesn't see article5 returned
        self.assertNotIn(self.test_article5, response.context['articles'])

    def test_dashboard_view_user_2(self):
        # Log in user2
        self.client.login(email=self.user2.email, password='djangopassword123')

        response = self.client.get(reverse('dashboard'))

        # Test how many articles are returned, user2 should see 4 because of group access
        self.assertEqual(len(response.context['articles']), 4)
        # Also check user2 can not see article1 returned
        self.assertNotIn(self.test_article1, response.context['articles'])

    def test_dashboard_view_user_3(self):
        # Log in user3
        self.client.login(email=self.user3.email, password='djangopassword123')

        response = self.client.get(reverse('dashboard'))

        # Test how many articles are returned, user3 should see all 5 because they are admin
        self.assertEqual(len(response.context['articles']), 5)
        # Also check user3 can see all articles
        self.assertIn(self.test_article1, response.context['articles'])
        self.assertIn(self.test_article2, response.context['articles'])
        self.assertIn(self.test_article3, response.context['articles'])
        self.assertIn(self.test_article4, response.context['articles'])
        self.assertIn(self.test_article5, response.context['articles'])

    def test_article_view_without_view_permission(self):
        # Log in user1
        self.client.login(email=self.user1.email, password='djangopassword123')

        # Test viewing article5, user1 should be redirected back to dashboard
        response = self.client.get(reverse('article', kwargs={'slug': self.test_article5.slug}))
        self.assertRedirects(response, reverse('dashboard'))

    def test_article_view_without_view_with_edit_permission(self):
        # Log in user2
        self.client.login(email=self.user2.email, password='djangopassword123')

        # Test viewing article4, user2 should be able to view it with edit despite not having view permission
        response = self.client.get(reverse('article', kwargs={'slug': self.test_article4.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['article'], self.test_article4)

    def test_edit_article_with_group_edit_permission(self):
        # Log in user2
        self.client.login(email=self.user2.email, password='djangopassword123')

        # Test POST request with valid data
        data = {
            'title': 'Updated Test Article',
            'content': 'New content',
        }
        self.client.post(reverse('edit-article', kwargs={'slug': self.test_article3.slug}), data=data)

        # Test title has updated
        self.test_article3.refresh_from_db()
        self.assertEqual(self.test_article3.title, data['title'])

    def test_edit_article_without_group_edit_permission(self):
        # Log in user2
        self.client.login(email=self.user2.email, password='djangopassword123')

        # Check user2 can view
        response = self.client.get(reverse('article', kwargs={'slug': self.test_article2.slug}))
        self.assertEqual(response.status_code, 200)

        # Test POST request with valid data
        data = {
            'title': 'Updated Test Article',
            'content': 'New content',
        }
        self.client.post(reverse('edit-article', kwargs={'slug': self.test_article2.slug}), data=data)

        # Test title has not updated
        self.test_article2.refresh_from_db()
        self.assertNotEqual(self.test_article2.title, data['title'])

    def test_delete_article_without_view_permission(self):
        # Log in user1
        self.client.login(email=self.user1.email, password='djangopassword123')

        # User 1 should not be able to view article 5 so should not be able to delete it either
        response = self.client.post(reverse('delete-article', kwargs={'slug': self.test_article5.slug}))
        # This should return permission denied
        self.assertEqual(response.status_code, 403)

        # Verify the article still exists
        self.assertTrue(Article.objects.filter(id=self.test_article5.id).exists())

    def test_delete_article_with_view_permission(self):
        # Log in user2
        self.client.login(email=self.user2.email, password='djangopassword123')

        # User 2 should be able to view article 2 but not edit or delete
        response = self.client.post(reverse('delete-article', kwargs={'slug': self.test_article2.slug}))
        # This should return permission denied
        self.assertEqual(response.status_code, 403)

        # Verify the article still exists
        self.assertTrue(Article.objects.filter(id=self.test_article2.id).exists())

    def test_delete_article_with_edit_permission(self):
        # Log in user2
        self.client.login(email=self.user2.email, password='djangopassword123')

        # User 2 should be able to edit and delete article3
        response = self.client.post(reverse('delete-article', kwargs={'slug': self.test_article3.slug}))
        self.assertRedirects(response, reverse('dashboard'))

        # Verify the article still exists
        self.assertFalse(Article.objects.filter(id=self.test_article3.id).exists())

    # Admins should be able to view, edit and delete anything without explicit permission
    # User 3 is an admin and does not exist in any of the test groups
    def test_admin_view_article_without_view_permission(self):
        # Log in user3
        self.client.login(email=self.user3.email, password='djangopassword123')

        response = self.client.get(reverse('article', kwargs={'slug': self.test_article5.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['article'], self.test_article5)

    def test_admin_edit_article_without_view_permission(self):
        # Log in user3
        self.client.login(email=self.user3.email, password='djangopassword123')

        # Test POST request with valid data
        data = {
            'title': 'Updated Test Article',
            'content': 'New content',
        }
        self.client.post(reverse('edit-article', kwargs={'slug': self.test_article1.slug}), data=data)

        # Test title has updated
        self.test_article1.refresh_from_db()
        self.assertEqual(self.test_article1.title, data['title'])

    def test_admin_delete_article_without_view_permission(self):
        # Log in user3
        self.client.login(email=self.user3.email, password='djangopassword123')

        response = self.client.post(reverse('delete-article', kwargs={'slug': self.test_article5.slug}))
        self.assertRedirects(response, reverse('dashboard'))

        # Verify article does not still exist
        self.assertFalse(Article.objects.filter(id=self.test_article5.id).exists())

