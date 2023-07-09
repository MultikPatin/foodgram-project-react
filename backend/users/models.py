from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    email = models.EmailField("Email", unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELDS = 'email'
    
    def __str__(self):
        return str(self.username)
