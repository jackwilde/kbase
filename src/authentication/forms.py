from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import Form, EmailField, EmailInput

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        error_messages = {
            'first_name': {
                'required': 'Please enter your first name',
            },
            'last_name': {
                'required': 'Please enter your last name',
            },
            'email': {
                'unique': 'This email is already in use',
                'required': 'Please enter your email address',
                'invalid': 'Enter a valid email address',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set placeholder text for each field
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

        # Mark fields as required
        for field in self.fields:
            self.fields[field].required = True


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
