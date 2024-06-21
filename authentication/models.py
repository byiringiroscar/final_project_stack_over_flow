from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from questions.models import Badge

from django.utils import timezone

now = timezone.now()


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("user must have an email address")
        if not full_name:
            raise ValueError("user must have full_name")
        if not phone_number:
            raise ValueError("Instructor must have phone_number")
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name, phone_number, password):
        if not email:
            raise ValueError("user must have an email address")
        if not full_name:
            raise ValueError("user must have full_name")
        if not phone_number:
            raise ValueError("Instructor must have phone_number")
        user = self.create_user(
            email,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password, **extra_fields):

        user = self.create_user(
            email,
            full_name,
            phone_number,
            password=password,
        )
        user.is_verified = True
        user.is_two_f_enable = False
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone_number = PhoneNumberField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_two_f_enable = models.BooleanField(default=False)

    # username = None

    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']
    objects = UserManager()

    class Meta:
        app_label = 'authentication'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def get_profile_image(self):
        image = self.profile.user_image.url
        return image

    @property
    def get_profile_location(self):
        location = self.profile.location
        return location

    @property
    def get_badge_status(self):
        all_badge = Badge.objects.all()
        list_all_badge = [all_badge.user.email for all_badge in all_badge]
        if self.email in list_all_badge:
            return True
        else:
            return False


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    user_image = models.ImageField(upload_to='images/', default='profile.png', null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    github_link = models.URLField(default='https://github.com/', null=True, blank=True)
    website_link = models.URLField(default='https://www.google.com/', null=True, blank=True)
    backend_development = models.PositiveIntegerField(null=True, blank=True)
    frontend_development = models.PositiveIntegerField(null=True, blank=True)
    hardware = models.PositiveIntegerField(null=True, blank=True)
    uiandux = models.PositiveIntegerField(null=True, blank=True)
    artificial_intelligence = models.PositiveIntegerField(null=True, blank=True)
    badge = models.BooleanField(default=False)
    date_created = models.DateField(default=now)

    def __str__(self):
        return f'{self.user.full_name} -- {self.user.phone_number}'
