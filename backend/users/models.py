from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator


class User(AbstractUser):
    ADMIN = "admin"
    roles = (
        (ADMIN, ADMIN),
    )
    username_validator = UsernameValidator()
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    email = models.EmailField(
        "Email",
        max_length=254,
        unique=True
    )
    role = models.CharField(
        "Роль пользователя",
        choices=roles,
        max_length=255,
        default=None
    )

    def __str__(self):
        return str(self.username)
    
    @property
    def is_admin(self):
        return self.role == self.ADMIN
