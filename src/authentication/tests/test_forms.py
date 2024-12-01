from django.test import TestCase
from authentication.models import User
from authentication.forms import SignUpForm, SignInForm

class SignUpFormTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='existinguser@example.com',
            first_name='Existing',
            last_name='User',
            password='djangopassword123'
        )


    def test_form_valid(self):
        # Test form is valid with correct data
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'djangopassword123',
            'password2': 'djangopassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_first_name(self):
        # Test form errors with empty first name
        form_data = {
            'first_name': '',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'djangopassword123',
            'password2': 'djangopassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertEqual(form.errors['first_name'], ['Please enter your first name'])

    def test_form_invalid_first_name(self):
        # Test form errors with invalid first name
        form_data = {
            'first_name': 'T3s+',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'djangopassword123',
            'password2': 'djangopassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertEqual(form.errors['first_name'], ['First name can only contain letters'])

    def test_form_empty_last_name(self):
        # Test form errors with empty last name
        form_data = {
            'first_name': 'Test',
            'last_name': '',
            'email': 'testuser@example.com',
            'password1': 'djangopassword123',
            'password2': 'djangopassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertEqual(form.errors['last_name'], ['Please enter your last name'])

    def test_form_invalid_last_name(self):
        # Test form errors with invalid last name
        form_data = {
            'first_name': 'Test',
            'last_name': 'U5€r',
            'email': 'testuser@example.com',
            'password1': 'djangopassword123',
            'password2': 'djangopassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)
        self.assertEqual(form.errors['last_name'], ['Last name can only contain letters'])

    def test_form_empty_email(self):
        # Test form errors with empty email
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': '',
            'password1': 'djangopassword123',
            'password2': 'djangopassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Please enter your email address'])

    def test_form_invalid_email(self):
        # Test form errors with invalid email
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser.example.com',
            'password1': 'djangopassword123',
            'password2': 'djangopassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['Enter a valid email address'])

    def test_form_duplicate_email(self):
        # Test form errors with duplicate email
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'existinguser@example.com',
            'password1': 'djangopassword123',
            'password2': 'djangopassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ['This email is already in use'])

    def test_form_empty_passwords(self):
        # Test form errors with empty passwords
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': '',
            'password2': '',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
        self.assertEqual(form.errors['password1'], ['This field is required.'])
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['This field is required.'])

    def test_form_mismatched_passwords(self):
        # Test form errors with mismatched passwords
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'djangopassword123',
            'password2': 'djangopassword12',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['The two password fields didn’t match.'])

    def test_form_common_passwords(self):
        # Test form errors with common passwords
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'password',
            'password2': 'password',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['This password is too common.'])

    def test_form_short_passwords(self):
        # Test form errors with short passwords
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'a1874bc',
            'password2': 'a1874bc',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['This password is too short. It must contain at least 8 characters.'])

    def test_form_numeric_passwords(self):
        # Test form errors with numeric only passwords
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': '87619387112',
            'password2': '87619387112',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['This password is entirely numeric.'])

    def test_form_similar_passwords(self):
        # Test form errors with password similar to email
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'testuser123',
            'password2': 'testuser123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertEqual(form.errors['password2'], ['The password is too similar to the email.'])

class SignInFormTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            email='existinguser@example.com',
            first_name='Existing',
            last_name='User',
            password='djangopassword123'
        )

    def test_form_valid(self):
        # Test form is valid with existing user
        form_data = {
            'username': 'existinguser@example.com',
            'password': 'djangopassword123',
        }
        form = SignInForm(data=form_data)
        self.assertTrue(form.is_valid())
        print(form.errors)

    def test_form_invalid(self):
        # Test form is invalid with incorrect user details
        form_data = {
            'username': 'testuser@example.com',
            'password': 'djangopassword123',
        }
        form = SignInForm(data=form_data)
        self.assertFalse(form.is_valid())
