from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, SelectMultiple
from authentication.models import Group, User


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = [
            'name',
            'users',
        ]
        labels = {
            'name': 'Group name',
            'users': 'Members',
        }
        widgets = {
            'name': TextInput(attrs={
                'id': 'input-title',
                'placeholder': 'Group Name',
            }),
            'users': SelectMultiple(attrs={
                'id': 'select-members',
            }),
        }
        error_messages = {
            'name': {
                'unique': 'A group with that name already exists',
            },
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If your User model has a ManyToManyField to Group,
        # you can dynamically set the queryset for users to show all available users
        self.fields['users'].queryset = User.objects.all()
        self.fields['users'].widget.choices = [
            (user.id, f"{user.full_name} <{user.email}>") for user in self.fields['users'].queryset
        ]

    def clean_name(self):
        name = self.cleaned_data['name'].lower()
        return name
