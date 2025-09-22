from django.db import models

class Promotion(models.Model):
    description = models.CharField(max_length=255) 
    discount = models.FloatField()
    
    
    

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL,null=True,related_name='+')

# Create your models here.
class Product(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description =  models.TextField()
    unit_price =  models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection  = models.ForeignKey(Collection, on_delete=models.PROTECT) #one to one or many to one relationship
    promotions = models.ManyToManyField(Promotion) #many to many relationships
    

class Customer(models.Model):
    
    MEMBERSHIP_CHOICES_BRONZE = 'B'
    MEMBERSHIP_CHOICES_SILVER = 'S'
    MEMBERSHIP_CHOICES_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_CHOICES_BRONZE,'Bronze'),
        (MEMBERSHIP_CHOICES_SILVER,'Silver'),
        (MEMBERSHIP_CHOICES_GOLD,'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1,choices = MEMBERSHIP_CHOICES,default=MEMBERSHIP_CHOICES_BRONZE)
    

    
class Order(models.Model):
    
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    status_choices = [
        (PAYMENT_STATUS_PENDING, 'pending'),
        (PAYMENT_STATUS_COMPLETE,'complete'),
        (PAYMENT_STATUS_FAILED,'failed'),
    ]
    
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1,choices=status_choices,default = PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # Items = models.ForeignKey(Item,on_delete=models.CASCADE)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    zip = models.CharField(max_length=100,null=True)
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    