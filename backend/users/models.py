from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    first_name = models.CharField(verbose_name='first name', max_length=256)
    last_name = models.CharField(verbose_name='last name', max_length=256)
    email = models.EmailField(
        verbose_name='email address', max_length=256, unique=True
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
