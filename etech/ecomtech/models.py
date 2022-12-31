from django.db import models
# Create your models here.
class Customer(models.Model):
  cust_lname=models.CharField(max_length=200,null=True)
  cust_fname=models.CharField(max_length=200,null=True)
  cust_email=models.EmailField(max_length=200,null=True)
  cust_password=models.CharField(max_length=20,null=True)
  cust_address=models.TextField(null=True)
  cust_image=models.ImageField(max_length=200,upload_to='customers/',null=True)
  cust_phone=models.CharField(max_length=20,null=True)
  date_joined=models.DateField(auto_now=True)

class Product(models.Model):
  class ProductCategoryChoice(models.TextChoices):
    LAPTOP='Laptop'
    ACCESSORIES='Acessories'
    PHONES='Phones'
    TABLET='Tablet'
    CAMERAS='Camera'
  class ManufacturerNameChoice(models.TextChoices):
    APPLE='Apple'
    SAMSUNG='Samsung'
    AMAZON='Amazon'
    SONY='Sony'
    DELL='Dell'
    HP='HP'
    NOKIA='Nokia'
  product_name=models.CharField(max_length=100,null=True)
  stock_no=models.IntegerField(null=True)
  prod_image=models.ImageField(max_length=200,upload_to='products/',null=True)
  manufacturer_name=models.CharField(max_length=50,null=True,choices=ManufacturerNameChoice.choices)
  category=models.CharField(max_length=50,null=True,choices=ProductCategoryChoice.choices)
  product_description=models.TextField(null=True)
  product_price=models.FloatField(max_length=11,null=True)
  slug=models.SlugField(unique=True,db_index=True,null=True)

  def __str__(self) :
     return f'{self.product_name} {self.category} {self.manufacturer_name}'

class Newsletter(models.Model):
  email=models.EmailField(max_length=100,null=True)
  date_subscribed=models.DateField(auto_now=True)

class Review():
  review_by=models.CharField(max_length=50,null=True)
  review_email=models.EmailField(max_length=50,null=True)
  review_content=models.TextField(null=True)
  review_for=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL,related_name='prod_rev')
  review_date=models.DateField(auto_now=True)

class Cart(models.Model):
  cust_id=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL,related_name='cartdeets')
  product_name=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL,related_name='prod_cart')
  quantity_added=models.IntegerField(null=True,default='1')
  date_added=models.DateField(auto_now=True)

class Wishlist(models.Model):
  cust_id=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL,related_name='wishdeets')
  product_name=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL,related_name='prod_wish')
  date_added=models.DateField(auto_now=True)

class Transaction(models.Model):
    class TransactionStatusChoices(models.TextChoices):
      PENDING='pending'
      FAILED='failed'
      PAID='paid'

    class TransactionMethodChoices(models.TextChoices):
      CARD='card'
      CASH='cash'
    
    trx_customer = models.ForeignKey(Customer, null=True,on_delete=models.SET_NULL,related_name='cust_trx')
    trx_refno= models.CharField(max_length=200,null=True)
    trx_totalamt = models.ForeignKey(Product, null=True,on_delete=models.SET_NULL,related_name='prod_trx')
    trx_status = models.CharField(max_length=50,null=True,choices=TransactionStatusChoices.choices)
    trx_method= models.CharField(max_length=50,null=True,choices=TransactionMethodChoices.choices)
    trx_paygate=models.TextField(null=True)
    trx_date=models.DateTimeField(auto_now=True)
    trx_expiry=models.DateTimeField(null=True)