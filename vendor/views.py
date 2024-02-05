from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import viewsets,status
from rest_framework.response import Response
from core import settings
from .models import *
from .serializer import *
from django.db import connection
from rest_framework.parsers import MultiPartParser,FormParser


@api_view(['GET','POST','PUT'])    
def vendorV(requests):
    if requests.method == 'GET':
        try:
            vendor_data = Vendor.objects.all()
            serializers = VendorSerializer(vendor_data,many=True)
            return Response(serializers.data,
                            status=status.HTTP_200_OK
                            )
            
        except Exception as e:
            return Response({"message":str(e)})    
    
@api_view(["GET", "POST","PUT","DELETE"])
def CategoryV(request):
    if request.method == "GET":
        try:
            parent = request.GET.get("parent", "")
            if parent != "":
                categories = Category.objects.filter(parent=parent)
                serializer = CategorySerializer(categories, many=True)
                return Response({"serializer": serializer.data},
                                status=status.HTTP_200_OK
                                )
    
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK
                            )
        except Exception as e:
            return Response({"message":str(e)})
    
    elif request.method == "POST":
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED
                                )
        except Exception as e:
            return Response({"message":str(e)})    
    
    elif request.method == "PUT":
        try:
            data = request.data
            obj = Category.objects.get(id=data["id"])
            serializer = CategorySerializer(obj,data=data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Data updated successfully ","Data":serializer.data},
                                status=status.HTTP_200_OK
                                )
            
            return Response({"Error":serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
    
    elif request.method == "DELETE":
        try:
            delete = request.GET.get('delete')
            if delete:
                c_obj = Category.objects.get(id=delete)
                c_obj.delete()
            return Response({'message':'Data deleted successfully'},
                            status=status.HTTP_200_OK
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
  
@api_view(['GET','POST','PUT','DELETE'])
def marketV(requests,id=None):
    search = requests.GET.get('search')
    data = []
    if requests.method == 'GET':
        try:
            if search:
                m_obj = Market.objects.filter(name__icontains = search)
                for obj in m_obj:
                    data.append({'market_name':obj.name})
                return Response({'data':data},
                                status=status.HTTP_200_OK
                                )
                
            elif id == None:
                market_obj = Market.objects.all()
                serializers = MarketSerializer(market_obj,many=True)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            else :
                market_obj = Market.objects.get(id=id)
                serializers = MarketSerializer(market_obj)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
        
        except Exception as e:
            return Response({"message":str(e)})        
    
    elif requests.method == 'POST':
        try:
            data = requests.data 
            city_obj = City.objects.get(id=data['city_id'])
            market_obj = Market.objects.create(name=data['name'],
                                               city_id=city_obj,
                                               image=data['image'])
            market_obj.save()
            serializers=MarketSerializer(market_obj)
            return Response (serializers.data,
                             status=status.HTTP_201_CREATED
                             )
        
        except Exception as e:
            return Response({"message":str(e)})
    
    elif requests.method == 'PUT':
        try:
            data = requests.data
            m_obj = Market.objects.get(id=data['id']) 
            serializers= MarketSerializer(m_obj,data=data)
            
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            return Response(serializers.errors,
                            status=status.HTTP_400_BAD_REQUEST
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
    
    elif requests.method == 'DELETE':
        try:
            delete = requests.GET.get('delete')
            if delete:
                m_obj = Market.objects.get(id=delete)
                m_obj.delete()
            return Response({'message':'Data deleted successfully'},
                            status=status.HTTP_200_OK
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
    
@api_view(['GET','POST','PUT','DELETE'])    
def shopV(requests,id=None):
    search = requests.GET.get('search')
    data = []
    if requests.method == 'GET':
        try:
            if search:
                s_obj = Shop.objects.filter(shop_name__icontains=search)
                for obj  in s_obj:
                    data.append({'Shop_name':obj.shop_name})
                    return Response({'data':data},
                                    status=status.HTTP_200_OK
                                    )
                  
            elif id==None:
                s_obj = Shop.objects.all()
                serializers = ShopSerializer(s_obj , many=True)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            else :
                s_obj =Shop.objects.get(id=id)
                serializers = ShopSerializer(s_obj)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
            
    
    elif requests.method == 'POST':
        parser_classes = [MultiPartParser,FormParser]
        try:
            data = requests.data 
            c_obj = City.objects.get(id=data['city_id'])
            m_obj = Market.objects.get(id=data['market_id'])
            v_obj = Vendor.objects.get(id=data['vendor_id'])
            s_obj = Shop.objects.create(shop_name=data['shop_name'],
                                        market_id=m_obj,
                                        city_id=c_obj,
                                        vendor_id=v_obj,
                                        image=data['image'])
            s_obj.save()
            serializers = ShopSerializer(s_obj)
            return Response(serializers.data,
                            status=status.HTTP_201_CREATED
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
         
    elif requests.method == 'PUT':
        try:
            data = requests.data 
            s_obj = Shop.objects.get(id=data['id'])
            serializers = ShopSerializer(s_obj,data=data) 
            if serializers.is_valid():
                serializers.save() 
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})
             
    elif requests.method == 'DELETE':
        try:
            delete = requests.GET.get('delete')
            if delete:
                s_obj = Shop.objects.get(id=delete)
                s_obj.delete()
            return Response({'message':'Data deleted successfully'},
                            status=status.HTTP_200_OK
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
        
        
       
@api_view(['GET','POST','PUT','DELETE'])    
def productV(requests,slug=None):
    search = requests.GET.get('search')
    data = []
    if requests.method == 'GET':
        try:
            if slug == None:
              product_data = Product.objects.all()
              serializers = ProductSerializer(product_data,many=True)
              return Response(serializers.data,
                              status=status.HTTP_200_OK
                              )
            elif search:
                p_obj = Product.objects.filter(name__icontains=search)
                for obj in p_obj:
                    data.append({'Product_name':obj.name})
                    return Response({'data':data},
                                    status=status.HTTP_200_OK
                                    )  
            else:
                product_data = Product.objects.get(slug=slug)
                serializers = ProductSerializer(product_data)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
          
    elif requests.method == 'POST':
        try:
            data = requests.data 
            s_obj = Shop.objects.get(id=data['shop_id'])
            c_obj = Category.objects.get(id=data['category_id'])
            void_obj = Variation_option.objects.get(id=data['VOID'])
            shop_outlet_obj = Shop_outlet.objects.get(id=data['shop_outlet_id'])
            product_obj = Product.objects.create(product_name=data['product_name'],
                                                  description=data['description'],
                                                  price=data['price'],
                                                  last_price=data['last_price'],
                                                  shop_id=s_obj,
                                                  category_id=c_obj,
                                                  shop_outlet_id=shop_outlet_obj,
                                                  VOID=void_obj
                                                  ) 
            product_obj.save()
            serializers = ProductSerializer(product_obj)
            return Response(serializers.data,
                            status=status.HTTP_201_CREATED
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
         
    elif requests.method == 'PUT':
        try:
            product_data = Product.objects.get(slug=slug)
            serializers = ProductSerializer(product_data,data=requests.data)  
            if serializers.is_valid():
                serializers.save()
                
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})       
        
    elif requests.method == 'DELETE':
        try:
            delete = requests.GET.get('delete')
            if delete:
                product_data = Product.objects.get(slug=delete)
                product_data.delete()
            return Response({'message':'Data deleted successfully'},
                            status=status.HTTP_200_OK
                            )
            
        except Exception as e:
            return Response({"message":str(e)})
        
            
@api_view(['GET','POST'])    
def product_imageV(requests,id=None):
    if requests.method == 'GET':
        try:
            if id == None:
                P_I_obj = Product_image.objects.all()
                serializers = Product_imageSerializer(P_I_obj,many=True)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            else:
                p_obj = Product_image.objects.get(id=id)
                serializers = Product_imageSerializer(P_I_obj)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
        except Exception as e:
            return Response({"message":str(e)})    
        
    elif requests.method == 'POST':
        try:
            data=requests.data
            p_obj = Product.objects.get(id=data['product_id'])
            product_image = Product_image.objects.create(url=data['url'],product_id=p_obj)
            product_image.save()
            
            serializers = Product_imageSerializer(product_image)
            return Response(serializers.data,
                            status=status.HTTP_201_CREATED
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
        
    elif requests.method == 'PUT':
        try:
            data = requests.data
            product_image_obj = Product_image.objects.get(id=data['id'])
            serializers = Product_imageSerializer(product_image_obj)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
         
    elif requests.method == 'DELETE':
        try:
            delete = requests.GET.get('delete')
            if delete:
                p_image = Product_image.objects.get(id=delete)
                p_image.delete()
            return Response({'message':'Data deleted successfully'},
                            status=status.HTTP_200_OK
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
        

@api_view(['GET','POST','PUT','DELETE'])    
def shop_outletV(requests,id=None):
    # search = requests.GET.get('search')
    # data = []
    if requests.method == 'GET':
        try:
            if id == None:
              shop_outlet_obj = Shop_outlet.objects.all()
              serializers = Shop_outletSerializer(shop_outlet_obj,many=True)
              return Response(serializers.data,
                              status=status.HTTP_200_OK
                              )
            # elif search:
            #     s_o_obj = Shop_outlet.objects.filter(name__icontains=search)
            #     for obj in s_o_obj:
            #         data.append({'Shop_outlet_name':obj.name})
            #         return Response({'data':data},
            #                         status=status.HTTP_200_OK
            #                         )  
            else:
                shop_outlet_obj = Shop_outlet.objects.get(id=id)
                serializers = Shop_outletSerializer(shop_outlet_obj)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
          
    elif requests.method == 'POST':
        try:
            data = requests.data 
            s_obj = Shop.objects.get(id=data['shop_id'])
            shop_outlet_obj = Shop_outlet.objects.create(landmark=data['landmark'],
                                                  latitude=data['latitude'],
                                                  longitude=data['longitude'],
                                                  postal_code=data['postal_code'],
                                                  is_default=data['is_default'],
                                                  address_type=data['address_type'],
                                                  address_line1=data['address_line1'],
                                                  shop_id=s_obj,
                                                  ) 
            shop_outlet_obj.save()
            serializers = Shop_outletSerializer(shop_outlet_obj)
            return Response(serializers.data,
                            status=status.HTTP_201_CREATED
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
         
    elif requests.method == 'PUT':
        try:
            data=requests.data
            shop_outlet_data = Shop_outlet.objects.get(id=data['id'])
            print('\n',shop_outlet_data,'\n')
            serializers = Shop_outletSerializer(shop_outlet_data,data=data)  
            if serializers.is_valid():
                serializers.save()
                
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})       
        
    elif requests.method == 'DELETE':
        try:
            delete = requests.GET.get('delete')
            if delete:
                shop_outlet_data = Shop_outlet.objects.get(id=delete)
                shop_outlet_data.delete()
            return Response({'message':'Data deleted successfully'},
                            status=status.HTTP_200_OK
                            )
            
        except Exception as e:
            return Response({"message":str(e)})




@api_view(['GET','POST','PUT','DELETE'])    
def variationV(requests,id=None):
    # search = requests.GET.get('search')
    # data = []
    if requests.method == 'GET':
        try:
            if id == None:
              variation_obj = Variation.objects.all()
              serializers = VariationSerializer(variation_obj,many=True)
              return Response(serializers.data,
                              status=status.HTTP_200_OK
                              )
            # elif search:
            #     s_o_obj = Variation.objects.filter(name__icontains=search)
            #     for obj in s_o_obj:
            #         data.append({'Variation_name':obj.name})
            #         return Response({'data':data},
            #                         status=status.HTTP_200_OK
            #                         )  
            else:
                variation_obj = Variation.objects.get(id=id)
                serializers = VariationSerializer(variation_obj)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
          
    elif requests.method == 'POST':
        try:
            data = requests.data 
            category_id_obj = Category.objects.get(id=data['category_id'])
            variation_obj = Variation.objects.create(name=data['name'],
                                                  category_id=category_id_obj,
                                                  ) 
            variation_obj.save()
            serializers = VariationSerializer(variation_obj)
            return Response(serializers.data,
                            status=status.HTTP_201_CREATED
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
         
    elif requests.method == 'PUT':
        try:
            data=requests.data
            variation_obj = Variation.objects.get(id=data['id'])
            serializers = VariationSerializer(variation_obj,data=data)  
            if serializers.is_valid():
                serializers.save()
                
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})       
        
    elif requests.method == 'DELETE':
        try:
            delete = requests.GET.get('delete')
            if delete:
                variation_obj = Variation.objects.get(id=delete)
                variation_obj.delete()
            return Response({'message':'Data deleted successfully'},
                            status=status.HTTP_200_OK
                            )
            
        except Exception as e:
            return Response({"message":str(e)})

@api_view(['GET','POST','PUT','DELETE'])    
def variation_optionV(requests,id=None):
    # search = requests.GET.get('search')
    # data = []
    if requests.method == 'GET':
        try:
            if id == None:
              variation_option_obj = Variation_option.objects.all()
              serializers = Variation_optionSerializer(variation_option_obj,many=True)
              return Response(serializers.data,
                              status=status.HTTP_200_OK
                              )
            # elif search:
            #     s_o_obj = Variation_option.objects.filter(name__icontains=search)
            #     for obj in s_o_obj:
            #         data.append({'Variation_option_name':obj.name})
            #         return Response({'data':data},
            #                         status=status.HTTP_200_OK
            #                         )  
            else:
                variation_option_obj = Variation_option.objects.get(id=id)
                serializers = Variation_optionSerializer(variation_option_obj)
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})    
          
    elif requests.method == 'POST':
        try:
            data = requests.data 
            varition_id_obj = Variation.objects.get(id=data['varition_id'])
            variation_option_obj = Variation_option.objects.create(value=data['value'],
                                                  varition_id=varition_id_obj,
                                                  ) 
            variation_option_obj.save()
            serializers = Variation_optionSerializer(variation_option_obj)
            return Response(serializers.data,
                            status=status.HTTP_201_CREATED
                            )
        
        except Exception as e:
            return Response({"message":str(e)})
         
    elif requests.method == 'PUT':
        try:
            data=requests.data
            variation_option_obj = Variation_option.objects.get(id=data['id'])
            serializers = Variation_optionSerializer(variation_option_obj,data=data)  
            if serializers.is_valid():
                serializers.save()
                
                return Response(serializers.data,
                                status=status.HTTP_200_OK
                                )
            
        except Exception as e:
            return Response({"message":str(e)})       
        
    elif requests.method == 'DELETE':
        try:
            delete = requests.GET.get('delete')
            if delete:
                variation_option_obj = Variation_option.objects.get(id=delete)
                variation_option_obj.delete()
            return Response({'message':'Data deleted successfully'},
                            status=status.HTTP_200_OK
                            )
            
        except Exception as e:
            return Response({"message":str(e)})

























##----------------------Extra Part--------------------------------------





@api_view(['GET'])
def shop_outlettestV(request):
    try:
        if request.method == 'GET':
            outlet_obj = Shop_outlet.objects.select_related('shop_id').all()
            print('\n\n\n',outlet_obj,'\n\n\n')
            print(outlet_obj[0].shop_id.image)
            outlet_data=[]
            for obj in outlet_obj:
                outlet = obj.products.all()
                print('\n\n\n',outlet,'\n\n\n')
                product_serializers = ProductSerializer(outlet,many=True)
                outlet_data.append({
                    'outlet': Shop_outletSerializer(obj).data,
                    'products': product_serializers.data
                })
            print(connection.queries)
            return Response(outlet_data)          
            
    except Exception as e:
            return Response({"message":str(e)})        
        
@api_view(['GET'])
def shop_outlettest(request):
    try:
        if request.method == 'GET':
            outlet_obj = Shop_outlet.objects.get(id=1)
            print('\n\n\n',outlet_obj,'\n\n\n')
            outlet = outlet_obj.products.all()
            print('\n\n\n',outlet.query,'\n\n\n')
            outlet_data = {
                'outlet': Shop_outletSerializer(outlet_obj).data,
                'products': ProductSerializer(outlet,many=True).data
            }
            outlet_data = Shop_outletSerializer(outlet_obj).data
            outlet_data['products'] = ProductSerializer(outlet,many=True).data
            return Response(outlet_data)          
            
    except Exception as e:
            return Response({"message":str(e)})         