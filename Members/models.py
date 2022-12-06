from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Member(User):
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
