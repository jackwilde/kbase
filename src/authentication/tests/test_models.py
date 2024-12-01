from django.test import TestCase

from django_knowledgebase.settings import SECRET_KEY
from authentication.models import User, Group
from django.core.exceptions import ValidationError, PermissionDenied

# Create your tests here.
class UserModelTestCase(TestCase):
    def setUp(self):
        # Get all users group for testing
        self.all_users_group = Group.objects.get(name="all users")

    def test_create_user(self):
        # Test creating a user
        user = User.objects.create_user(
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="securepassword123"
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.full_name, "Test User")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertIn(self.all_users_group, user.groups.all())
        self.assertEqual(user.is_admin, False)


    # def test_create_user_without_email(self):
    #     # Test user creation without an email should raise ValueError
    #     with self.assertRaises(ValueError):
    #         User.objects.create_user(
    #             email="",
    #             first_name="Test",
    #             last_name="User",
    #             password="securepassword123"
    #         )
    #
    # def test_create_user_without_first_name(self):
    #     # Test user creation without first name should raise ValueError
    #     with self.assertRaises(ValueError):
    #         User.objects.create_user(
    #             email="testuser@example.com",
    #             first_name="",
    #             last_name="User",
    #             password="securepassword123"
    #         )
    #
    # def test_create_user_without_last_name(self):
    #     # Test user creation without last name should raise ValueError
    #     with self.assertRaises(ValueError):
    #         User.objects.create_user(
    #             email="testuser@example.com",
    #             first_name="Test",
    #             last_name="",
    #             password="securepassword123"
    #         )
    #
    # def test_user_str_method(self):
    #     # Test string representation of the user
    #     user = User.objects.create_user(
    #         email="testuser@example.com",
    #         first_name="Test",
    #         last_name="User",
    #         password="securepassword123"
    #     )
    #     self.assertEqual(str(user), "testuser@example.com")
    #
    # def test_all_users_group_protection(self):
    #     # Test that "All Users" group cannot be edited or deleted
    #     with self.assertRaises(PermissionDenied):
    #         self.all_users_group.delete()
    #
    #     with self.assertRaises(PermissionDenied):
    #         self.all_users_group.name = "New Name"
    #         self.all_users_group.save()