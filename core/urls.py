from django.contrib import admin
from django.urls import path , include
from core import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from vendor.views import *

router = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/',include('customer.urls')),
    path('user/',include('auth_user.urls')),
    path('vendor/',include('vendor.urls')),
]


urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)