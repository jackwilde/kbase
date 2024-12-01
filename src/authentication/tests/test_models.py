from django.test import TestCase
from authentication.models import User, Group
from django.core.exceptions import ValidationError, PermissionDenied

class UserModelTestCase(TestCase):
    def setUp(self):
        # Get all users group for testing
        self.all_users_group = Group.objects.get(name='all users')

    def test_create_user(self):
        # Test creating a user
        user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertTrue(user.check_password('djangopassword123'))
        self.assertIn(self.all_users_group, user.groups.all())
        self.assertEqual(user.is_admin, False)

    def test_delete_user(self):
        # Test deleting a user
        user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123'
        )
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())
        user.delete()
        self.assertFalse(User.objects.filter(email='testuser@example.com').exists())

    def test_edit_user(self):
        # Test editing a user
        user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123'
        )
        # Test user before edit
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertTrue(user.check_password('djangopassword123'))
        self.assertIn(self.all_users_group, user.groups.all())
        self.assertEqual(user.is_admin, False)

        # Edit the user
        user.first_name = 'Account'
        user.last_name = 'Test'
        user.is_admin = True
        user.email = 'accountest@example.com'
        user.password = 'newpassword123'
        user.save()

        # Test user after edit
        edited_user = User.objects.get(email='accountest@example.com')
        self.assertEqual(edited_user.first_name, 'Account')
        self.assertEqual(edited_user.last_name, 'Test')
        self.assertEqual(edited_user.is_admin, True)
        self.assertEqual(edited_user.email, 'accountest@example.com')
        self.assertEqual(edited_user.password, 'newpassword123')

    def test_create_user_without_email(self):
        # Test creating a user without email raises ValidationError
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='',
                first_name='Test',
                last_name='User',
                password='djangopassword123'
            )

    def test_create_user_without_first_name(self):
        # Test creating a user without first name raises ValidationError
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='testuser@example.com',
                first_name='',
                last_name='User',
                password='djangopassword123'
            )

    def test_create_user_without_last_name(self):
        # Test creating a user without last name raises ValidationError
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='testuser@example.com',
                first_name='Test',
                last_name='',
                password='djangopassword123'
            )

    def test_create_user_with_duplicate_email(self):
        # Test creating a user with duplicate email raises ValidationError
        User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123'
        )
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='testuser@example.com',
                first_name='Second',
                last_name='User',
                password='djangopassword321'
            )

    def test_create_user_with_invalid_first_name(self):
        # Test creating a user with invalid first name raises ValidationError
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='testuser@example.com',
                first_name='T3<5T',
                last_name='User',
                password='djangopassword123'
            )

    def test_create_user_with_invalid_last_name(self):
        # Test creating a user with invalid first name raises ValidationError
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='testuser@example.com',
                first_name='Test',
                last_name='U5€R',
                password='djangopassword123'
            )

    def test_create_user_with_invalid_email(self):
        # Test creating a user with invalid email raises ValidationError
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='testuser@example.com',
                first_name='Test',
                last_name='U5€R',
                password='djangopassword123'
            )

    def test_user_str_method(self):
        # Test object string
        user = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123'
        )
        self.assertEqual(str(user), 'testuser@example.com')


class GroupModelTestCase(TestCase):
    def setUp(self):
        # Create users to test with
        self.user1 = User.objects.create_user(
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

    def test_all_users_group_exists(self):
        # Test that 'All Users' group has been created
        group = Group.objects.get(name='all users')
        self.assertIsNotNone(group)

        # Test that it has the correct pk and name
        self.assertEqual(group.pk, 1)
        self.assertEqual(group.name, 'all users')

    def test_all_users_group_is_protected(self):
        group = Group.objects.get(name='all users')
        # Test that 'All Users' group cannot be renamed or deleted
        with self.assertRaises(PermissionDenied):
            group.delete()

        with self.assertRaises(PermissionDenied):
            group.name = 'New Name'
            group.save()

    def test_create_group(self):
        # Test creating a group
        group = Group.objects.create(name='new group')
        # Add some users
        group.users.add(self.user1, self.user2)
        self.assertEqual(group.name, 'new group')
        self.assertEqual(group.users.count(), 2)
        self.assertIn(self.user1, group.users.all())
        self.assertIn(self.user2, group.users.all())

    def test_create_group_with_duplicate_name(self):
        # Test creating a group with duplicate name raises ValidationError
        Group.objects.create(name='new group')
        with self.assertRaises(ValidationError):
            Group.objects.create(name='new group')

    def test_delete_group(self):
        group = Group.objects.create(name='new group')
        group.users.add(self.user1, self.user2)
        self.assertTrue(Group.objects.filter(name='new group').exists())
        group.delete()
        self.assertFalse(Group.objects.filter(name='new group').exists())

    def test_edit_group(self):
        group = Group.objects.create(name='new group')
        group.name = 'another group'
        group.save()
        self.assertEqual(group.name, 'another group')

