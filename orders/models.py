from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class MenuItem(models.Model):
    name = models.CharField(max_length=63)
    desc = models.CharField(max_length=1000, default='')
    price = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.name} {self.price}"

    @classmethod
    def create(cls, user, name, price, desc):
        menuItem = cls(user=user, name=name, price=price, desc=desc)
        return menuItem


class OrderItem(models.Model):
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)
    menuItemName = models.CharField(default='small', max_length=63)

    def __str__(self):
        return f"{self.menuItem}"

    @classmethod
    def create(cls, menuItem):
        orderitem = cls(menuItem=menuItem)
        return orderitem


class Order(models.Model):
    orderItems = models.ManyToManyField(OrderItem)
    totalPrice = models.FloatField(default=0)
    isConfirmed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    address = models.CharField(max_length=1000, default=False)
    name = models.CharField(max_length=100, default='', null=True)
    phone = models.CharField(max_length=12, default='', null=True)
    isPaid = models.BooleanField(default=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             related_name='user')
    sellerUser = models.ForeignKey(User,
                                   on_delete=models.CASCADE,
                                   null=True,
                                   related_name='sellerUser')
    isAccepted = models.BooleanField(default=False)
    isRejected = models.BooleanField(default=False)
    feedback = models.CharField(max_length=1000, null=True)
    rate = models.FloatField(validators=[MinValueValidator(0.0),
                             MaxValueValidator(5.0)],
                             null=True)

    @classmethod
    def create(cls, user, sellerUser, isPaid):
        order = cls(user=user,
                    sellerUser=sellerUser,
                    isPaid=isPaid,
                    date=datetime.now())
        return order


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000, blank=True)
    tel = models.CharField(max_length=12,  blank=True)
    address = models.CharField(max_length=120, blank=True)
    name = models.CharField(max_length=100, blank=True)
    rate = models.FloatField(validators=[MinValueValidator(0.0),
                             MaxValueValidator(5.0)],
                             default=2)
    imagePath = models.CharField(max_length=10000,
                                 blank=True,
                                 default='data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22286%22%20height%3D%22180%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%20286%20180%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_16a88aeb64e%20text%20%7B%20fill%3Argba(255%2C255%2C255%2C.75)%3Bfont-weight%3Anormal%3Bfont-family%3AHelvetica%2C%20monospace%3Bfont-size%3A14pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_16a88aeb64e%22%3E%3Crect%20width%3D%22286%22%20height%3D%22180%22%20fill%3D%22%23777%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%22107.1953125%22%20y%3D%2296.6%22%3E286x180%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E')

    @classmethod
    def create(cls, user):
        profile = cls(user=user)
        # do something with the book
        return profile
