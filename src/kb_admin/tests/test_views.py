from django.urls import reverse
from authentication.models import User, Group
from django.test import TestCase
from django.utils.crypto import get_random_string

"""
These tests focus on authenticated admin users.
Unauthenticated users and non-admin users are tested in ./test_urls.py
"""

# Generate a random user password for test accounts
TEST_USER_PASSWORD = get_random_string(length=24)

class AuthenticatedUrlsTestCase(TestCase):
    # These test authenticated non admin user. They should all redirect to standard dashboard
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            password=TEST_USER_PASSWORD,
        )
        self.user1.is_admin = True
        self.user1.save()
        self.user2 = User.objects.create_user(
            email='seconduser@example.com',
            first_name='Second',
            last_name='User',
            password=TEST_USER_PASSWORD
        )
        self.user3 = User.objects.create_user(
            email='thirduser@example.com',
            first_name='Third',
            last_name='User',
            password=TEST_USER_PASSWORD,
        )
        self.user3.is_admin = True
        self.user3.save()
        self.user4 = User.objects.create_user(
            email='fourthuser@example.com',
            first_name='Fourth',
            last_name='User',
            password=TEST_USER_PASSWORD
        )
        self.user5 = User.objects.create_user(
            email='fifthuser@example.com',
            first_name='Fifth',
            last_name='User',
            password=TEST_USER_PASSWORD
        )

        # Create test groups
        self.group1 = Group.objects.create(name='group 1')
        self.group1.users.add(self.user1, self.user2, self.user3)
        self.group2 = Group.objects.create(name='group 2')
        self.group2.users.add(self.user3, self.user4, self.user5)
        self.group3 = Group.objects.create(name='group 3')

        # Log user in
        self.client.login(email='testuser@example.com', password=TEST_USER_PASSWORD)

    def test_dashboard_admin_view(self):
        # Test sign in view returns the correct template successfully
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kb_admin/dashboard.html')

    def test_all_users_view(self):
        # Test all users view returns the correct template successfully
        response = self.client.get(reverse('all-users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kb_admin/users.html')

    def test_user_detail_view(self):
        # Test user details view returns the correct template successfully
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kb_admin/user-detail.html')

    def test_user_delete_view(self):
        # Test user delete view accepts post and deletes user
        test_user = self.user5
        response = self.client.post(reverse('user-delete', kwargs={'pk': test_user.pk}))
        self.assertRedirects(response, reverse('all-users'))
        self.assertFalse(User.objects.filter(pk=test_user.pk).exists())

    def test_user_delete_view_fails(self):
        test_user = self.user1
        # Test user delete view won't allow user to delete themselves
        response = self.client.post(reverse('user-delete', kwargs={'pk': test_user.pk}))

        # Test redirect back to user details
        self.assertRedirects(response, reverse('user-detail', kwargs={'pk': test_user.pk}))


    def test_set_permissions_view_add(self):
        # Test set_permissions view will make a non admin user an admin user
        test_user = self.user2
        # Confirm user is not admin
        self.assertFalse(test_user.is_admin)

        # Test POST
        response = self.client.post(reverse('set-permissions', kwargs={'pk': test_user.pk}))
        self.assertRedirects(response, reverse('user-detail', kwargs={'pk': test_user.pk}))

        # Confirm user is now admin
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_admin)

    def test_set_permissions_view_remove(self):
        # Test set_permissions view will make a non admin user an admin user
        test_user = self.user3
        # Confirm user is admin
        self.assertTrue(test_user.is_admin)

        # Test POST
        response = self.client.post(reverse('set-permissions', kwargs={'pk': test_user.pk}))
        self.assertRedirects(response, reverse('user-detail', kwargs={'pk': test_user.pk}))

        # Confirm user is not admin
        test_user.refresh_from_db()
        self.assertFalse(test_user.is_admin)

    def test_set_permissions_view_self(self):
        # Test set_permissions stops user removing their admin permission
        test_user = self.user1
        # Confirm user is admin
        self.assertTrue(test_user.is_admin)

        # Test POST
        response = self.client.post(reverse('set-permissions', kwargs={'pk': test_user.pk}))
        self.assertRedirects(response, reverse('user-detail', kwargs={'pk': test_user.pk}))

        # Confirm user is still admin
        test_user.refresh_from_db()
        self.assertTrue(test_user.is_admin)

    def test_all_groups_view(self):
        # Test all groups view returns the correct template successfully
        response = self.client.get(reverse('all-groups'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kb_admin/groups.html')

    def test_group_detail_view(self):
        # Test group details view returns the correct template successfully
        response = self.client.get(reverse('group-detail', kwargs={'pk': self.group2.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kb_admin/group-detail.html')

    def test_create_group_view(self):
        # Test that group is created using post
        response = self.client.get(reverse('create-group'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kb_admin/group-new-edit.html')
        self.assertNotIn('edit_mode', response.context)

        # Test POST
        data = {
            'name': 'Test Group',
            'users': [self.user1.pk, self.user2.pk, self.user3.pk],
        }
        response = self.client.post(reverse('create-group'), data)

        # Check group was created. String must be lower here because of clean method.
        self.assertTrue(Group.objects.filter(name=data['name'].lower()).exists())

        group = Group.objects.get(name=data['name'].lower())
        # Check it redirects correctly
        self.assertRedirects(response, reverse('group-detail', kwargs={'pk': group.pk}))

        # Check it contains the correct members
        self.assertListEqual(list(group.users.values_list('id', flat=True)), data['users'])

    def test_create_group_view_duplicate(self):
        # Test that trying to create a duplicate group fails
        total_groups_before = len(Group.objects.all())

        data = {
            'name': 'group 1',
            'users': [self.user1.pk, self.user2.pk],
        }
        response = self.client.post(reverse('create-group'), data)

        # Test status code is 200
        self.assertEqual(response.status_code, 200)

        total_groups_after = len(Group.objects.all())
        # Check the number of groups is the same before and after
        self.assertEqual(total_groups_before, total_groups_after)

    def test_group_edit_view(self):
        # Test group edit view can rename groups
        test_group = self.group3
        # Test group-edit returns the correct template
        response = self.client.get(reverse('group-edit', kwargs={'pk': test_group.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kb_admin/group-new-edit.html')
        self.assertTrue(response.context['edit_mode'])

        group_before = {
            'name': test_group.name,
            'users': test_group.users.values_list('id', flat=True),
        }

        # Test POST and redirect to detail
        data = {
            'name': 'New group Name',
            'users': [self.user1.pk, self.user2.pk],
        }
        response = self.client.post(reverse('group-edit', kwargs={'pk': test_group.pk}), data=data)
        self.assertRedirects(response, reverse('group-detail', kwargs={'pk': test_group.pk}))

        test_group.refresh_from_db()
        group_after = {
            'name': test_group.name,
            'users': test_group.users.values_list('id', flat=True),
        }

        # Test that group has changed
        self.assertNotEqual(group_before, group_after)

        # Test that group matches the entered data
        self.assertEqual(data['name'].lower(), test_group.name.lower())
        self.assertListEqual(data['users'], list(test_group.users.values_list('id', flat=True)))

    def test_group_edit_view_duplicate(self):
        # Test that trying to edit a group with a duplicate fails
        test_group = self.group3

        group_name_before = test_group.name

        data = {
            'name': 'group 1',
        }

        response = self.client.post(reverse('group-edit', kwargs={'pk': test_group.pk}), data=data)
        # Test status code is 200
        self.assertEqual(response.status_code, 200)

        test_group.refresh_from_db()
        group_name_after = test_group.name

        # Check the name hasn't changed
        self.assertEqual(group_name_before, group_name_after)

    def test_group_delete_view(self):
        # Test group delete view
        test_group = self.group3
        self.assertTrue(Group.objects.filter(name=test_group.name).exists())

        response = self.client.post(reverse('group-delete', kwargs={'pk': test_group.pk}))
        self.assertRedirects(response, reverse('all-groups'))

    ## Test all users group protection
    def test_all_users_group_edit(self):
        # Test that trying to edit all users group fails
        test_group = Group.objects.get(name='all users')

        group_name_before = test_group.name

        data = {
            'name': 'new all users',
        }

        response = self.client.post(reverse('group-edit', kwargs={'pk': test_group.pk}), data=data)
        # Test return Forbidden 403
        self.assertEqual(response.status_code, 403)

        test_group.refresh_from_db()
        group_name_after = test_group.name

        # Check the name hasn't changed
        self.assertEqual(group_name_before, group_name_after)

    def test_all_users_group_delete(self):
        # Test that trying to delete all users group fails
        test_group = Group.objects.get(name='all users')

        response = self.client.post(reverse('group-delete', kwargs={'pk': test_group.pk}))
        # Test return Forbidden 403
        self.assertEqual(response.status_code, 403)

        test_group.refresh_from_db()

        # Check the name hasn't changed
        self.assertTrue(Group.objects.filter(name=test_group.name).exists())