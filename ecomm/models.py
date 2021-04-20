from django.db import models
from django.conf import settings


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.brand_name


class Item(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.FloatField()
    discount_price = models.FloatField()

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.qty} of {self.item.title}"


class Address(models.Model):
    CITY_CHOICE = (("PURNEA", "PRNA"), ("PATNA", "PAT"), ("DELHI", "DEL"), ("MUMBAI", "MUM"), ("KOLKATA", "KOL"),)
    STATE_CHOICE = (("BIHAR", "BR"), ("JHARKHAND", "JHR"), ("MAHARASHTRA", "MHRSHTRA"), ("WEST BENGAL", "WB"), ("ODISHA", "ODSH"),)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=10,choices=CITY_CHOICE)
    state = models.CharField(max_length=20,choices=STATE_CHOICE)
    alternative_no = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=200, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
