from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from vendor.serializer import *
from vendor.models import *
from customer.serializer import *
from customer.models import *
from .models import *
from .serializer import *
from django.contrib.auth import logout, authenticate
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.data["username"]
                password = serializer.data["password"]
                print(f"Profile Name: {username}, Password: {password}")
                user = authenticate(username=username, password=password)
                print(f"Authenticated User: {user}")
                if user is None:
                    return Response(serializer.errors)

                try:
                    customer = Customer.objects.get(user=user)
                except Customer.DoesNotExist:
                    customer = None

                if customer:
                    try:
                        addresses = customer.user_address.all()
                        serializer = AddressSerializers(addresses, many=True)
                        address = serializer.data
                        print("\n\n\n", address, "\n\n\n")

                    except Address.DoesNotExist:
                        address = None
                else:
                    address = None

                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                custom_claims = access_token.get("custom_claims", {})

                custom_claims["user_id"] = user.id
                custom_claims["username"] = user.username
                custom_claims["first_name"] = user.first_name
                custom_claims["last_name"] = user.last_name

                if address:

                    custom_claims["address"] = address

                # access_token['custom_claims'] = custom_claims
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(access_token),
                        "user": custom_claims,
                    }
                )
            return Response(serializer.errors)

        except Exception as e:
            return Response({"message": str(e)})


@api_view(["GET", "POST", "DELETE", "PUT"])
def customer_userV(request):

    if request.method == "GET":
        try:
            user_obj = Customer.objects.all()
            serializer = CustomerSerializer(user_obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)})

    elif request.method == "POST":
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                user = CoreUser.objects.create(
                    username=validated_data["username"],
                    first_name=validated_data["first_name"],
                    last_name=validated_data["last_name"],
                    is_buyer="True",
                )
                user.set_password(validated_data["password"])
                user.save()
                customer = Customer.objects.create(
                    user=user,
                    phone_no=validated_data["phone_no"],
                    email=validated_data["email"],
                )
                serializer = CustomerSerializer(customer)
                return Response(
                    {"message": "User Resgitered Successfully", "success": True},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError as ie:
                return Response(
                    {"message": "User Already Exists", "success": False},
                    status=status.HTTP_409_CONFLICT,
                )
        return Response(serializer.errors)

    elif request.method == "PUT":
        try:
            data = request.data
            obj = Customer.objects.get(id=data["id"])
            serializer = CustomerSerializer(obj, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Data updated successfully ", "Data": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({"message": str(e)})

    elif request.method == "DELETE":
        try:
            delete = request.GET.get("delete")
            if delete:
                user_data = Customer.objects.get(id=delete)
                user_data.delete()
            return Response(
                {"message": "Data deleted successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"message": str(e)})


@api_view(["GET", "POST", "DELETE", "PUT"])
def vendoruserV(request):

    if request.method == "GET":
        try:
            user_obj = Vendor.objects.all()
            serializer = VendorSerializer(user_obj, many=True)
            return Response({"serializer": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)})

    elif request.method == "POST":
        serializer = VendorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data

                user = CoreUser.objects.create(
                    username=validated_data["username"],
                    first_name=validated_data["first_name"],
                    last_name=validated_data["last_name"],
                    is_seller="True",
                )
                user.set_password(validated_data["password"])
                user.save()
                vendor = Vendor.objects.create(
                    user=user,
                    phone_no=validated_data["phone_no"],
                    email=validated_data["email"],
                )
                serializer = VendorSerializer(vendor)

                return Response(
                    {"message": "User Resgitered Successfully", "success": True},
                    status=status.HTTP_201_CREATED,
                )

            except IntegrityError as ie:
                return Response(
                    {"message": "User Already Exists", "success": False},
                    status=status.HTTP_409_CONFLICT,
                )

    elif request.method == "PUT":
        try:
            data = request.data
            obj = Vendor.objects.get(id=data["id"])
            serializer = VendorSerializer(obj, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Data updated successfully ", "Data": serializer.data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response({"message": str(e)})

    elif request.method == "DELETE":
        try:
            delete = request.GET.get("delete")
            if delete:
                user_data = Vendor.objects.get(id=delete)
                user_data.delete()

            return Response(
                {"message": "Data deleted successfully"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"message": str(e)})


class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"Message": "Enter refresh_token"})
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Success"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)})


class PasswordReset(APIView):

    serializer_class = EmailSerializer

    def post(self, request):

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                username = serializer.data["username"]
                user = CoreUser.objects.filter(username=username).first()

                if user:
                    encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
                    token = PasswordResetTokenGenerator().make_token(user)
                    reset_url = reverse(
                        "reset-password",
                        kwargs={"encoded_pk": encoded_pk, "token": token},
                    )
                    reset_link = f"http://localhost:8000{reset_url}"

                    subject = "Reset password link"
                    message = f"Hi This is your reset password link - {reset_link}"
                    email = serializer.validated_data["email"]
                    from_mail = settings.EMAIL_HOST_USER
                    send_mail(subject, message, from_mail, [email])

                    return Response(
                        {"message": f"Your password reset link : {reset_link}"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "User doesn't exists"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": str(e)})


class Reset_passAPI(generics.GenericAPIView):
    serializer_class = Reset_PasswordSerializer

    def patch(self, request, *args, **kwargs):

        try:
            serializer = self.serializer_class(
                data=request.data, context={"kwargs": kwargs}
            )

            if serializer.is_valid():
                return Response(
                    {"message": "Password reset successfully"},
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": str(e)})


class ChangePasswordView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            serializer = Change_PasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = self.request.user
                if not user.check_password(serializer.data.get("old_password")):
                    return Response(
                        {"old_password": ["Wrong password."]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if serializer.data.get("new_password") != serializer.data.get(
                    "Againnew_password"
                ):
                    return Response(
                        {"new_password": ["Passwords do not match."]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.set_password(serializer.data.get("new_password"))
                user.save()
                return Response(
                    {"message": "Password successfully changed."},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": str(e)})
