from django.db import models
from auth_user.models import CoreUser
from customer.models import *
from .utils import generate_slug 
from mptt.models import MPTTModel, TreeForeignKey


class Vendor(models.Model):
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE, related_name="vender")
    email = models.EmailField(max_length=255,unique=True,null=True,blank=True)
    phone_no = models.CharField(max_length=20, unique=True,null=True,blank=True)

    class Meta:
        db_table = "vendor_user"   
        
    def __str__(self):
        return self.user.username

class Category(MPTTModel):
    title = models.CharField(max_length=255,blank=True, null=True)
    image = models.ImageField(upload_to="category/",blank=True, null=True)
    parent = TreeForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="children")

    def __str__(self):
        return self.title
    class Meta:
        db_table = "category"
    
    

class Market(models.Model):
    name = models.CharField(max_length=155)
    image = models.ImageField(upload_to="market/",)
    city_id = models.ForeignKey(City,on_delete=models.CASCADE)
    
    class Meta:
        db_table = "market" 
    
    def __str__(self):
        return self.name   
    
    
class Shop(models.Model):
    shop_name = models.CharField(max_length=155)
    image = models.ImageField(upload_to="Shop/",)
    market_id = models.ForeignKey(Market,on_delete=models.CASCADE)
    city_id = models.ForeignKey(City,on_delete=models.CASCADE)
    vendor_id = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    
    class Meta:
        db_table = "shop"
        
    def __str__(self):
        return self.shop_name
    
class Shop_outlet(models.Model):
    landmark = models.CharField(max_length=155)
    latitude = models.CharField(max_length=155)
    longitude = models.CharField(max_length=155)   
    postal_code = models.CharField(max_length=155)   
    is_default = models.BooleanField()
    address_type = models.CharField(max_length=155) 
    address_line1 = models.CharField(max_length=155) 
    shop_id = models.ForeignKey(Shop,on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.shop_id.shop_name
    
    class Meta:
        db_table = "shop_outlet"
    
class Product(models.Model):
    product_name = models.CharField(max_length=155)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    last_price = models.IntegerField()
    shop_id = models.ForeignKey(Shop,on_delete=models.CASCADE)  
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True, null=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    shop_outlet_id = models.ManyToManyField(Shop_outlet , related_name='products')
    VOID = models.ManyToManyField('Variation_option')
    
    def save(self,*args, **kwargs):
        self.slug = generate_slug(self.product_name)
        super(Product,self).save(*args, **kwargs)
    
    class Meta:
        db_table = "product"
    
    def __str__(self):
        return self.product_name
    
    
class Product_image(models.Model):
    url = models.ImageField(upload_to="Product_image/", default='default.jpg')
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    
    class Meta:
        db_table = "product_image"
        
    def __str__(self):
        return self.product_id.product_name    
  
    
    
class Variation(models.Model):
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE ,blank=True, null=True)    
    name = models.CharField(max_length=155)
    
    class Meta:
        db_table = "variation"
        
    def __str__(self):
        return self.name    
    
class Variation_option(models.Model):
    varition_id=models.ForeignKey(Variation,on_delete=models.CASCADE)
    value = models.CharField(max_length=155)
    
    class Meta:
        db_table = "variation_option"    
    
    
    def __str__(self):
        return self.value