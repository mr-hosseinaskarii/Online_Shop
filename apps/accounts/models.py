from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email_validator = RegexValidator(r'^[\w\.-]+@[\w\.-]+\.\w+$', 'Enter a valid email address')
    phone_validator = RegexValidator(r'^\+98(90|91|92|93|99)\d{8}$', 'Enter a valid phone number')
    password_validator = RegexValidator(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$',
        """Password must must meet these needs:
        - at least one capital letter -> A-Z
        - at least one small letter -> a-z
        - at least one symbol -> !@#$%^&*()_+]
        - more than 8 characters
        """
    )

    email = models.EmailField(unique=True, validators=[email_validator])
    phone_number = models.CharField(unique=True, max_length=12, validators=[phone_validator], null=True, blank=False)
    password = models.CharField(max_length=20, validators=[password_validator])
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(_("active"), default=False)
    opt_code = models.CharField(max_length=6, blank=True, null=True)
    opt_expiry = models.DateTimeField(blank=True, null=True)

    # access level
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # time of register and last login
    registered_on = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    street = models.CharField(max_length=60)
    no = models.IntegerField()
    postal_code = models.CharField(max_length=10)
