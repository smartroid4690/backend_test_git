
from django.utils.text import slugify
import uuid



def generate_slug(product_name:str)->str:
        from .models import Product
        product_name = slugify(product_name)
        while(Product.objects.filter(slug = product_name).exists()):
            product_name =f'{slugify(product_name)}-{str(uuid.uuid4())[:4]}'
        return product_name



# def upload_to(instance, filename):
#     return '{filename}'.format(filename=filename)    