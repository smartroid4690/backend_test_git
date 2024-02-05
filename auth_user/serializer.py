from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CoreUser
        exclude = ['password']

class CustomerRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    phone_no = serializers.CharField()
    password = serializers.CharField()       

class VendorRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    phone_no = serializers.CharField()
    password = serializers.CharField() 
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()        
        
class Reset_PasswordSerializer(serializers.Serializer):
        password = serializers.CharField()
        
        
        def validate(self,data):
            password = data.get("password")
            token = self.context.get("kwargs").get("token")
            encoded_pk = self.context.get("kwargs").get("encoded_pk")
            
            if token is None or encoded_pk is None:
                raise serializers.ValidationError("Missing data")
            
            pk = urlsafe_base64_decode(encoded_pk).decode()
            user = CoreUser.objects.get(pk=pk)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("The reset token is invalid")
            
            
            user.set_password(password)
            user.save()
            return data 
           
class Change_PasswordSerializer(serializers.Serializer):
    old_password =serializers.CharField()
    new_password = serializers.CharField()
    Againnew_password = serializers.CharField()         
    
    
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField() 
    
    
    