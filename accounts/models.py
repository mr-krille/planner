from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Extended user profile to include role field
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('employee', 'Employee'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return f"{self.user.username} - {self.role}"