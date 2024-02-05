from rest_framework import serializers
from .models import *
from customer.serializer import *

class VendorSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()
    
    class Meta:
        model = Vendor
        fields = '__all__'
        
    def update(self,instance,validated_data):
        user_profile_data = validated_data.pop('user', {})
        user_profile_instance = instance.user
        user_profile_instance.username = user_profile_data.get('username', user_profile_instance.username)
        user_profile_instance.first_name = user_profile_data.get('first_name', user_profile_instance.first_name)
        user_profile_instance.last_name = user_profile_data.get('last_name', user_profile_instance.last_name)
        user_profile_instance.save()
        
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
         
                
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'        
        
class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__' 
        
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'                  
        
class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ['last_price']
        
class Product_imageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_image
        fields = '__all__'  
        
class Shop_outletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop_outlet
        fields = '__all__'                           
        
class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'        
        
class Variation_optionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation_option
        fields = '__all__'        