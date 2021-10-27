from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        #overiding BaseUserManager
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Creating a user """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ creating a user with super user status """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class AbstractEmailUser(AbstractUser):
    email = models.EmailField('Email Address', unique=True)
    username = None
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    __original_email = None

    def __init__(self, *args, **kwargs):
        super(AbstractEmailUser, self).__init__(*args, **kwargs)
        self.__original_email = self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class User(AbstractEmailUser):
    """ User Model """
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_full_name() or self.email