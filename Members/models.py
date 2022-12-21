from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe


# Create your models here.

class Member(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'

    def __str__(self):
        return self.username


class MemberImage(models.Model):
    image = models.ImageField(upload_to='images/', blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_image', null=True)

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'

    def __str__(self):
        return self.image.url


class MemberAddress(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_adress')
    street = models.CharField(max_length=200, null=True)
    number = models.CharField(max_length=5, null=True)
    postalcode = models.IntegerField(null=True)
    city = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=30, null=True)
