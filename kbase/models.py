from django.db import models
from django.utils.text import slugify

from authentication.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_articles')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modified_articles')
    modified_date = models.DateTimeField(auto_now=True)
    # images = models.ManyToManyField('Image', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def can_user_edit(self, user):
        return user == self.modified_by or user == self.created_by


    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class Image(models.Model):
#     image = models.ImageField(upload_to='media/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_images')
#
#     def __str__(self):
#         return self.image.name
