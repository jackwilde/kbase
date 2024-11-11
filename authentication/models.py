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
    groups = models.ManyToManyField('Group', related_name="users", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.email


class Group(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.name