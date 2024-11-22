from django.core.exceptions import ValidationError, PermissionDenied
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a new user
        :param email: Email address
        :param first_name: First Name
        :param last_name: Last Name
        :param password: Password
        :return: user object
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a new superuser
        :param email: Email address
        :param first_name: First Name
        :param last_name: Last Name
        :param password: Password
        :return: user object
        """
        user = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Add the user to "All Users' group if not already a member
        group = Group.objects.get(pk=1)
        if not self.groups.filter(pk=group.pk).exists():
            self.groups.add(group)

    def __str__(self):
        return self.email


class Group(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, unique=True)
    users = models.ManyToManyField('User', related_name="groups", blank=True)

    def save(self, *args, **kwargs):
        # Prevent edit of 'All Users' group
        if self.id == 1:
            raise PermissionDenied("The 'All Users' group cannot be altered.")
        self.name = self.name.lower()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Prevent deletion of 'All Users' group
        if self.id == 1:
            raise PermissionDenied("The 'All Users' group cannot be deleted.")
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name.title()