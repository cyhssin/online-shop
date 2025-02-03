from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """ UserManager: Custom manager for User model.
        Handles creating regular users and superusers with email,
                        names, and password. Validates required fields """

    def create_user(self, email, sur_name, for_name, password):

        if not email:
            raise ValueError("user must have email")

        if not sur_name:
            raise ValueError("user must have sur_name")

        if not for_name:
            raise ValueError("user must have for name")

        user = self.model(email=self.normalize_email(email),
                                                        sur_name=sur_name, for_name=for_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, sur_name, for_name, password):
        user = self.create_user(email, sur_name, for_name, password)
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user