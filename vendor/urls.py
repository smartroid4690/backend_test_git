from django.urls import path , include
from vendor import views
from .views import *
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static


router = DefaultRouter()

urlpatterns = router.urls
urlpatterns = [
    path('v_user/',views.vendorV),
    path('market/',views.marketV),
    path('market/<int:id>/',views.marketV),
    path('category/',views.CategoryV),
    path('shop/',views.shopV),
    path('shop/<int:id>/',views.shopV),
    path('product/',views.productV),
    path('product/<slug>/',views.productV),
    path('p_image/',views.product_imageV),
    path('shop_outlet/',views.shop_outletV),
    path('variation/',views.variationV),
    path('variation_option/',views.variation_optionV),
    path('shop_outlettestV/',views.shop_outlettestV),
    path('shop_outlettest/',views.shop_outlettest),
    
    
]
