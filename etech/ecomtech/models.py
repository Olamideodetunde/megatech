from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager,PermissionsMixin
# Create your models here.
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a new superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
  cust_lname=models.CharField(max_length=200,null=True)
  cust_fname=models.CharField(max_length=200,null=True)
  email=models.EmailField(unique=True)
  cust_address=models.TextField(null=True)
  cust_image=models.ImageField(max_length=200,upload_to='customers/',null=True)
  cust_phone=models.CharField(max_length=20,null=True)
  date_joined=models.DateField(auto_now=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  objects=CustomUserManager()
  USERNAME_FIELD='email'
  REQUIRED_FIELDS=[]
class ProductCategory(models.Model):
  prod_category_name=models.CharField(max_length=200,null=True)
  def __str__(self) :
    return f'{self.prod_category_name}'
    # LAPTOP='Laptop'
    # ACCESSORIES='Acessories'
    # PHONES='Phones'
    # TABLET='Tablet'
    # CAMERAS='Camera'
class ProductManufacturer(models.Model):
  prod_manufacturer_name=models.CharField(max_length=200,null=True)
   
    # APPLE='Apple'
    # SAMSUNG='Samsung'
    # AMAZON='Amazon'
    # SONY='Sony'
    # DELL='Dell'
    # HP='HP'
    # NOKIA='Nokia'
  def __str__(self) :
    return f'{self.prod_manufacturer_name}'
class Product(models.Model):
  product_name=models.CharField(max_length=100,null=True)
  stock_no=models.IntegerField(null=True)
  prod_image=models.ImageField(max_length=200,upload_to='products/',null=True)
  prod_manufacturer_name=models.ForeignKey(ProductManufacturer,null=True,on_delete=models.SET_NULL,related_name='prod_manufact')
  category=models.ForeignKey(ProductCategory,null=True,on_delete=models.SET_NULL,related_name='prod_category')
  product_description=models.TextField(null=True)
  product_price=models.FloatField(max_length=11,null=True)
  added_to_wishlist=models.BooleanField(null=True)
  slug=models.SlugField(unique=True,db_index=True,null=True)

  def __str__(self) :
     return f'{self.product_name} {self.category} {self.prod_manufacturer_name}'

class Newsletter(models.Model):
  email=models.EmailField(max_length=100,null=True)
  date_subscribed=models.DateField(auto_now=True)

class Review(models.Model):
  review_by=models.CharField(max_length=50,null=True)
  review_email=models.EmailField(max_length=50,null=True)
  review_content=models.TextField(null=True)
  review_ratings=models.IntegerField(null=True)
  review_for=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL,related_name='prod_rev')
  review_date=models.DateField(auto_now=True)

class Cart(models.Model):
  cust_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='cartdeets')
  products=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL,related_name='prod_cart')
  quantity_added=models.IntegerField(null=True,default='1')
  total_amt=models.FloatField(null=True)
  date_added=models.DateField(auto_now=True)

class Wishlist(models.Model):
  wishers_deets=models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='wishdeets')
  product_name=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL,related_name='prod_wish')
  date_added=models.DateField(auto_now=True)
class Checkout(models.Model):
  cust_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name='checkoutdeets')
  zip_code=models.CharField(max_length=50,null=True)
  country=models.CharField(max_length=50,null=True)
  city=models.CharField(max_length=50,null=True)
class Transaction(models.Model):
    class TransactionStatusChoices(models.TextChoices):
      PENDING='pending'
      FAILED='failed'
      PAID='paid'

    class TransactionMethodChoices(models.TextChoices):
      CARD='card'
      CASH='cash'
    
    trx_customer = models.ForeignKey(User, null=True,on_delete=models.SET_NULL,related_name='cust_trx')
    trx_refno= models.CharField(max_length=200,null=True)
    trx_totalamt = models.CharField(max_length=50,null=True)
    trx_status = models.CharField(max_length=50,null=True,choices=TransactionStatusChoices.choices)
    trx_method= models.CharField(max_length=50,null=True,choices=TransactionMethodChoices.choices)
    trx_paygate=models.TextField(null=True)
    trx_date=models.DateTimeField(auto_now=True)