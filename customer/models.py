from django.db import models
from auth_user.models import CoreUser




class Customer(models.Model):
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE, related_name="user")
    email = models.EmailField(max_length=255,unique=True,null=True,blank=True)
    phone_no = models.CharField(max_length=20, unique=True,null=True,blank=True)
    

    class Meta:
        db_table = "customer_users"
        
    def __str__(self):
        return self.user.username    

class Country(models.Model):
   
    countryCode = models.CharField(max_length=2, default='')
    countryName = models.CharField(max_length=100, default='')
    currencyCode = models.CharField(max_length=3, null=True, blank=True)
    telephonePrefix = models.CharField(max_length=10, default='')
    
    
    class Meta:
        db_table = "country"
        
     

    def __str__(self):
        return self.countryName

class City(models.Model):
    name = models.CharField(max_length=155)
    country_id =models.ForeignKey(Country,on_delete=models.CASCADE)
     
    
    class Meta:
        db_table = "city"
    
    def __str__(self):
        return self.name
    
class Address(models.Model):
       user_id = models.ForeignKey(Customer,on_delete=models.CASCADE ,related_name="user_address")
       poc_name=models.CharField(max_length=155,null=True,blank=True)
       poc_phone=models.CharField(max_length=155,null=True,blank=True)
       poc_email=models.EmailField(max_length=155,null=True,blank=True)
       flat_no = models.CharField(max_length=155)
       house_no = models.CharField(max_length=155)
       landmark = models.CharField(max_length=155)
       postal_code = models.CharField(max_length=40)
       city_id = models.ForeignKey(City,on_delete=models.CASCADE)
       country_id = models.ForeignKey(Country,on_delete=models.CASCADE)
       is_default = models.BooleanField(default=False)
       address_type = models.CharField(max_length=155)
       address_line1 = models.CharField(max_length=155) 
       
       class Meta:
           db_table = "address" 
        
        
       def __str__(self):
           return self.poc_name         


 