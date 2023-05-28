from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class UserManager(BaseUserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            return ValueError("The given email must be set")
        
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if extra_fields.get("is_superuser") == True:
            return ValueError("Regular users must have is_superuser=False.")
        if extra_fields.get("is_staff") == True:
            return ValueError("Regular users must have is_staff=False.")
        if extra_fields.get("is_active") == True:
            raise ValueError("Regular users must have is_active=False.")

        return self._create_user(name, email, password, **extra_fields)
 
    def create_superuser(self, name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(name, email, password, **extra_fields)



class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    
    email = models.EmailField(max_length=250, null=False, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return f'{self.name}'
