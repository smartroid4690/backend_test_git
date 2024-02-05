from django.contrib import admin
from django.urls import path , include
from .views import *
from auth_user import views
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)  

urlpatterns = [
   path('customer_signup/',views.customer_userV),
   path('vendor_signup/',views.vendoruserV),
   path('login/', LoginView.as_view()),
   path('logout/',Logout.as_view()),
   path('reset_email/',PasswordReset.as_view()),
   path('reset_password/<str:encoded_pk>/<str:token>/',Reset_passAPI.as_view(),name="reset-password"),
   path('changepassword/',ChangePasswordView.as_view()),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
