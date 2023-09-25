from django.db import models

from account.models import User


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs', blank=True, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images", null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(Category, blank=True, related_name='catt')
    title = models.CharField(max_length=30)
    text = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    img = models.ImageField(upload_to="images", null=True)
    size = models.ManyToManyField(Size, blank=True, related_name="products")
    color = models.ManyToManyField(Color, related_name="products")

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply', null=True, blank=True)

    def __str__(self):
        return self.body[:10]


class Information(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name="informations")
    text = models.TextField()

    def __str__(self):
        return self.text
