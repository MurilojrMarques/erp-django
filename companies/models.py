from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("accounts.Users", on_delete=models.CASCADE)