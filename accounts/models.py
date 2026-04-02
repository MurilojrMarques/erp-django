from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

class Users(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)

    def __str__(self):
        return self.email

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, related_name='custom_group_permissions_set', blank=True)

    def __str__(self):
        return self.name

class UserGroup(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)