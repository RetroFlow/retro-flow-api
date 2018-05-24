import jwt
import uuid

from datetime import datetime, timedelta

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models

import logging

logger = logging.Logger(__name__)


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, email, password=None, **kwargs):
        """Create and return a `User` with an email and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        normalized_email = self.normalize_email(email)
        username = normalized_email.split("@")[0]
        kwargs['username'] = username
        logger.info("username:  " + username)
        logger.info("normalized email:  " + normalized_email)

        user = self.model(email=normalized_email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    jwt_secret = models.UUIDField(default=uuid.uuid4)

    username = models.CharField(db_index=True, max_length=255, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(default=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'email'

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name.
        """
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        if self.first_name:
            return self.first_name
        else:
            return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, str(self.jwt_secret), algorithm='HS256')

        return token.decode('utf-8')

    def logout(self):
        """
        Generated new jwt secret. After this previous JWT token will be invalid
        """
        self.jwt_secret = uuid.uuid4()
        self.save()
