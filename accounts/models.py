from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STAFF)

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_staff_member(self):
        return self.role == self.Role.STAFF
