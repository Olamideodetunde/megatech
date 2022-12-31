from django.contrib import admin
from .models import Product,Cart,Transaction,Customer
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
  list_display=['product_name','category','manufacturer_name']
admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Transaction)
admin.site.register(Customer)