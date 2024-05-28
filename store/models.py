from django.db import models
from django.contrib.auth.models import User
import datetime
import os
from django.utils import timezone

def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)


# Create your models here.
class Category(models.Model):
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    descriptions = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default , 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default , 1=Trending")
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_descriptions = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.CharField(max_length=150, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    product_image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    product_image1 = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    product_image2 = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    product_image3 = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    product_image4 = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    small_descriptions = models.CharField(max_length=250, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    descriptions = models.TextField(max_length=500, null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default , 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default , 1=Trending")
    tag = models.CharField(max_length=150, null=False, blank=False)
    meta_title = models.CharField(max_length=150, null=False, blank=False)
    meta_keywords = models.CharField(max_length=150, null=False, blank=False)
    meta_descriptions = models.TextField(max_length=500, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False,default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phonenumber = models.CharField(max_length=50, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    orderstatuses = (
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Completed','Completed'),
    )
    status = models.CharField(max_length=150,choices=orderstatuses,default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return '{}' - '{}'.format(self.id, self.tracking_no)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_no)


class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=50, default=True)
    address = models.CharField(max_length=50, default=True)
    city = models.CharField(max_length=150, default=True)
    state = models.CharField(max_length=150, default=True)
    country = models.CharField(max_length=150, default=True)
    pincode = models.CharField(max_length=150, default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, null=True)
    comment = models.TextField(max_length=250, default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)



