from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = [
    ("admin", "Administrator"),
    ("employee", "Employee"),
]


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    email = models.EmailField("Email", unique=True)

    def __str__(self):
        return self.get_full_name()


class UserProfile(models.Model):
    """
    Extended user profile to include role field
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")

    def __str__(self):
        return f"{self.user.username} - {self.role}"
