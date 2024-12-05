from django.contrib.auth.models import AnonymousUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify

from authentication.models import User, Group


# Create your models here.
class Article(models.Model):
    title = models.CharField(unique=True, max_length=100,
                             validators=[
                                 RegexValidator(
                                     regex=r'^[\w\s-]+$',
                                     message='Title can only contain letters, numbers, spaces, hyphens, and underscores.',
                                 )
                             ])
    slug = models.SlugField(unique=True, max_length=100)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_articles')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_articles')
    modified_date = models.DateTimeField(auto_now=True)
    groups_with_view = models.ManyToManyField(Group, blank=True, related_name='groups_view_articles')
    groups_with_edit = models.ManyToManyField(Group, blank=True, related_name='groups_edit_articles')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_permissions(self, user):
        """
        Check the permissions of a given user against the Article

        Parameters
        ----------
        user : object
            user object to check

        Returns
        -------
        User permission for the article either None, view or edit
        """
        # Deny anonymous users
        if isinstance(user, AnonymousUser):
            return None
        # Permit the creator
        if user == self.created_by:
            return 'edit'
        # Permit admin users
        if user.is_admin:
            return 'edit'

        # Helper function to check if user belongs to any given group set
        def check_membership(groups):
            return groups.filter(id__in=user.groups.values_list('id', flat=True)).exists()

        # Permit users in can_view groups
        if check_membership(self.groups_with_edit):
            return 'edit'
        if check_membership(self.groups_with_view):
            return 'view'
        # Explicitly deny everything else
        return None

    def __str__(self):
        return self.title
