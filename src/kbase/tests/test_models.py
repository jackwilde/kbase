from django.test import TestCase
from django.utils.text import slugify
from django.utils import timezone
from authentication.models import User, Group
from django.core.exceptions import ValidationError
from kbase.models import Article
from django.utils.crypto import get_random_string

# Generate a random user password for test accounts
TEST_USER_PASSWORD = get_random_string(length=24)

class ArticleModelTestCase(TestCase):
    def setUp(self):
        # Create some users
        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            first_name='One',
            last_name='User',
            password=TEST_USER_PASSWORD
        )
        self.user2 = User.objects.create_user(
            email='testuser2@example.com',
            first_name='Two',
            last_name='User',
            password=TEST_USER_PASSWORD
        )

        # Create some groups
        self.group1 = Group.objects.create(
            name='testgroup1'
        )
        self.group2 = Group.objects.create(
            name='testgroup2'
        )

        # Create some articles
        self.test_article1 = Article.objects.create(
            title='Test Article 1',
            content='Test Content',
            created_by=self.user1,
        )
        self.test_article1.save()

        # This article should be viewable by owner, group2 (user2) and admin (user3)
        self.test_article2 = Article.objects.create(
            title='Test Group 2 View Article',
            content='Test Content',
            created_by=self.user2,
        )
        self.test_article2.groups_with_view.set([self.group2.id])
        self.test_article2.save()

    def test_create_article(self):
        article = Article.objects.create(
            title='New Article 1',
            content='Content for the first article',
            created_by=self.user1,
        )
        now = timezone.now()
        article.groups_with_view.set([self.group1, self.group2])
        article.groups_with_edit.set([self.group1])
        article.save()

        self.assertEqual(article.title, 'New Article 1')
        self.assertEqual(article.content, 'Content for the first article')
        self.assertEqual(article.created_by, self.user1)
        self.assertEqual(list(article.groups_with_view.all()), [self.group1, self.group2])
        self.assertEqual(list(article.groups_with_edit.all()), [self.group1])
        self.assertEqual(article.slug, slugify('New Article 1'))
        self.assertAlmostEqual(article.created_date, now, delta=timezone.timedelta(seconds=1))


    def test_create_article_empty_title(self):
        article = Article.objects.create(
            title='',
            content='Content for the first article',
            created_by=self.user1,
        )
        self.assertRaises(ValidationError, article.full_clean)

    def test_create_article_invalid_title(self):
        article = Article.objects.create(
            title='Test Title <>',
            content='Content for the first article',
            created_by=self.user1,
        )
        self.assertRaises(ValidationError, article.full_clean)
