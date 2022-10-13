from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
import re
from django.core.validators import RegexValidator

# Create your models here.
class CustomManager(BaseUserManager):
    def isValid(self, s):
        pattern = re.compile("(0|91)?[7-9][0-9]{9}")
        return pattern.match(s)

    def create_users(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")

        #if not (self.isValid(extra_fields["phone_number"])):
         #   raise ValueError("Number is invalid")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.create_users(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_users(username, email, password, **extra_fields)


user_types = (
    ('user', 'user'),
    ('seller', 'seller')
)


class User(AbstractUser):
    profile_dp = models.ImageField(upload_to="user/dp", blank=True,
                                   validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg',))])
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be contains only digits. Also Up to 10 digits allowed.")
    phone_number = models.CharField(
        _('phone no.'), max_length=10, blank=False, unique=False, validators=[phone_regex])
    user_type = models.CharField(
        _('user role'), max_length=20, choices=user_types, default='user')
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "profile_dp", "phone_number"]

    def __str__(self):
        return self.username
