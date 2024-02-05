
from django.utils.text import slugify
import uuid



def generate_slug(name:str)->str:
        from .models import City
        name = slugify(name)
        while(City.objects.filter(slug = name).exists()):
            name =f'{slugify(name)}-{str(uuid.uuid4())[:4]}'
        return name