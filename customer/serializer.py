from rest_framework import serializers
from .models import *
from auth_user.serializer import *
from rest_framework.response import Response 


class CustomerSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()
    
    class Meta:
        model = Customer
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



class CountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = "__all__"  
        
class CitySerializer(serializers.ModelSerializer):
    country_id = CountrySerializer(read_only=True)
    class Meta:
        model = City
        fields = "__all__" 
        
class AddressSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = "__all__"        