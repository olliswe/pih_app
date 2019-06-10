from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)




class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, position, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            position = position
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name,  last_name, position, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            position=position,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, position, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            position=position,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# hook in the New Manager to our Model
class User(AbstractBaseUser): # from step 2
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name="First name", max_length=225)
    last_name = models.CharField(verbose_name="Last name", max_length=225)
    position = models.CharField(verbose_name="Position", max_length=225)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that's built in.
    reviewer = models.BooleanField(default=False, verbose_name="Reviewer")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','position']  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name + ' ('+self.position+')'

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.first_name + ' ' + self.last_name + ' ('+self.position+')'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, pih_app):
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
    def is_active(self):
        "Is the user active?"
        return self.active

    @property
    def is_reviewer(self):
        return self.reviewer

    @property
    def is_submitter(self):
        return self.submitter



    objects = UserManager()