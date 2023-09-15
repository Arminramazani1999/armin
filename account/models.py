from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an email address")

        user = self.model(
            phone=self.normalize_email(phone),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="آدرس ایمیل",
        max_length=255,
        null=True,
        unique=True,
    )
    fullname = models.CharField(max_length=50, verbose_name="نام کامل")
    rpassword = models.CharField(max_length=40, null=True, blank=True)
    # date_of_birth = models.DateField()
    # user faal ast ya admin ast
    phone = models.CharField(max_length=12, unique=True, null=True, verbose_name='شماره موبایل')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')
    is_paid = models.BooleanField(default=False)

    objects = UserManager()
    # ahraz hoyet
    USERNAME_FIELD = "phone"
    # fild hayi ke zarori hastan
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone)

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
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    token = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expiration_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    fullname = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=30)

    def __str__(self):
        return self.user.phone


# class Registe_User(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     p
#     email = models.EmailField(null=True, blank=True)
