from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.text import slugify

from authentication.models import User, Group

# Create your models here.
class Article(models.Model):
    title = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_articles')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_articles')
    modified_date = models.DateTimeField(auto_now=True)
    groups_with_view = models.ManyToManyField(Group, blank=True, related_name='groups_view_articles')
    groups_with_edit = models.ManyToManyField(Group, blank=True, related_name='groups_edit_articles')
    # images = models.ManyToManyField('Image', blank=True)

    def save(self, *args, **kwargs):
        # If a group can edit make sure it gets view permissions
        for group in self.groups_with_edit.all():
            self.groups_with_view.add(group)

        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_permissions(self, user):
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


class Tag(models.Model):
    tag = models.CharField(max_length=25, unique=True)

    def save(self, *args, **kwargs):
        # Convert tag to lowercase before saving
        self.tag = self.tag.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tag


# class Image(models.Model):
#     image = models.ImageField(upload_to='media/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_images')
#
#     def __str__(self):
#         return self.image.name
