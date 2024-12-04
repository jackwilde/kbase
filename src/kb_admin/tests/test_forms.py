from authentication.models import User, Group
from kb_admin.forms import GroupForm
from django.test import TestCase

class SignUpFormTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password='djangopassword123',
        )
        self.user1.is_admin = True
        self.user1.save()
        self.user2 = User.objects.create_user(
            email='seconduser@example.com',
            first_name='Second',
            last_name='User',
            password='djangopassword123'
        )
        self.user3 = User.objects.create_user(
            email='thirduser@example.com',
            first_name='Third',
            last_name='User',
            password='djangopassword123',
        )

        # Create test groups
        self.group1 = Group.objects.create(name='group 1')
        self.group1.users.add(self.user1, self.user2, self.user3)
        self.group2 = Group.objects.create(name='group 2')
        self.group2.users.add(self.user3)
        self.group3 = Group.objects.create(name='group 3')

        # Log user in
        self.client.login(email='testuser@example.com', password='djangopassword123')

    def test_form_valid(self):
        # Test form is valid with correct data
        form_data = {
            'name': 'New Group',
            'users': [self.user1, self.user2],
        }
        form = GroupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_name(self):
        # Test form errors with empty first name fails
        form_data = {
            'name': '',
            'users': [self.user1, self.user2],
        }
        form = GroupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['This field is required.'])

    def test_form_empty_users(self):
        # Test form errors with empty users name passes
        form_data = {
            'name': 'New Group',
            'users': '',
        }
        form = GroupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_users(self):
        # Test form errors with invalid users name fails
        form_data = {
            'name': 'New Group',
            'users': ['user1', 'user2'],
        }
        form = GroupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_duplicate_group_name(self):
        # Test form errors with duplicate group name fails
        form_data = {
            'name': 'group 1',
        }
        form = GroupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['A group with that name already exists'])

