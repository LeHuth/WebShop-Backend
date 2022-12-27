from django.utils.safestring import mark_safe
from datetime import date
from Members.models import Member
from django.db import models

# Create your models here.
GENDER_CHOICE = [
    ('MEN', 'MEN'),
    ('WOMAN', 'WOMAN'),
    ('UNISEX', 'UNISEX')
]


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'

    def __str__(self):
        return self.name


class Stock(models.Model):
    name = models.TextField(max_length=50, editable=True)
    value = models.IntegerField(blank=False, default=0)
    in_stock = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Stock'

    def __str__(self):
        return self.name + ' (' + str(self.value) + ')'


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    stock = models.IntegerField(null=True, blank=True, default=0)
    gender = models.CharField(choices=GENDER_CHOICE, null=True, max_length=7, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, null=True)
    short_description = models.TextField(max_length=200, null=True, blank=True)
    long_description = models.TextField(max_length=1000, null=True, blank=True)
    variants = models.ManyToManyField(
        'self', null=True, blank=True,
        related_name='variant'
    )

    class Meta:
        verbose_name = 'Product'

    def __str__(self):
        if self.gender:
            return self.name + ' ' + self.gender
        else:
            return  self.name



class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')

    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{0}" width="150" height="150" />'.format(self.image.url))
        else:
            return '(No image)'

    def __str__(self):
        return self.image.url


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='product_review')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, related_name='review_owner')
    title = models.CharField(max_length=100, blank=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=False)
    text = models.TextField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.title + " - " + self.product.name


class Vote(models.Model):
    value = models.BooleanField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='vote_owner')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_vote')

    def __str__(self):
        return str(self.value) + ' on ' + self.review.title + ' by ' + self.member.username
