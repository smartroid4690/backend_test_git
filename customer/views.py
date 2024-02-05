from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *


@api_view(['GET'])
def countryV(requests):
    search = requests.GET.get('search')
    data = []
    if requests.method == 'GET':
        try:
            if search :
                c_obj = Country.objects.filter(countryName__startswith = search)
                for obj in c_obj:
                  data.append({'countryName':obj.countryName})
                  
                return Response({'data':data},
                                status=status.HTTP_200_OK
                                )
             
            else: 
                country_data = Country.objects.all()
                serializers = CountrySerializer(country_data,many=True)
            
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
        
        except Exception as e:
            return Response({"message":str(e)})    
    
    
@api_view(['GET','POST','PUT'])    
def cityV(requests,id=None):
    if requests.method == 'GET':
        try:
            if id==None:
                city_data = City.objects.all()
                serializers = CitySerializer(city_data,many=True)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            else:
                city_data = City.objects.get(id=id)
                serializers =CitySerializer(city_data)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
    
    elif requests.method == 'POST':
        try:
            data = requests.data 
            c_obj = Country.objects.get(id=data['country_id'])
            city_obj = City.objects.create(name=data['name'],
                                           country_id=c_obj) 
            city_obj.save()
            serializers = CitySerializer(city_obj)
            return Response(serializers.data,
                            status=status.HTTP_201_CREATED
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
         
    elif requests.method == 'PUT':
        
        try:
            city_data = City.objects.get(id=id)
            serializers = CitySerializer(city_data,data=requests.data)  
            if serializers.is_valid():
                serializers.save()
                
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
        

@api_view(['GET','POST','PUT'])        
def addressV(requests,id=None):
    
    if requests.method == 'GET':
        try:
            if id == None:
                address_obj = Address.objects.all()
                serializers = AddressSerializers(address_obj,many=True)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            else:
                address_obj = Address.objects.get(id=id)
                serializers = AddressSerializers(address_obj)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
          
    elif requests.method == 'POST':
        try:
            data = requests.data 
            user_obj = Customer.objects.get(id=data['user_id'])
            city_obj = City.objects.get(id=data['city_id'])
            country_obj = Country.objects.get(id=data['country_id'])
            address_obj = Address.objects.create(user_id =user_obj,
                                                 poc_name =data['poc_name'],
                                                 poc_phone =data['poc_phone'],
                                                 poc_email =data['poc_email'],
                                                 flat_no =data['flat_no'],
                                                 house_no =data['house_no'],
                                                 landmark =data['landmark'],
                                                 postal_code =data['postal_code'],
                                                 city_id =city_obj,
                                                 country_id =country_obj,
                                                 is_default =data['is_default'],
                                                 address_type =data['address_type'],
                                                 address_line1 =data['address_line1'],
                                                 )
            address_obj.save()
            serializers = AddressSerializers(address_obj)
            return Response(serializers.data,
                            status=status.HTTP_201_CREATED
                            ) 
        
        except Exception as e:
            return Response({"message":str(e)})
        
    elif requests.method == 'PUT':
        try:
            address_obj = Address.objects.get(id=id)
            serializers = AddressSerializers(address_obj,data=requests.data)
            if serializers.is_valid():
                serializers.save()
                
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
                
        except Exception as e:
            return Response({"message":str(e)})        
               
    
             