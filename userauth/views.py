from django.shortcuts import render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import jwt
from datetime import datetime
from .log import LOGGER, raise_400
from .authentication import IsTokenValid
from .models import UserModel, BlackListedToken

from .serializers import LoginSerializer

# Create your views here.

USER_ALREADY_PRESENT = "User Already Exist."
USER_NOT_EXIST = "User Does not Exist."

INVALID_LOGIN = "Invalid Username or Password."
class RegisterAPIView(APIView):

    """
    Register API
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get_serializer(self, *args, **kwargs):
        """Return view serializer class"""
        return self.serializer_class(*args, **kwargs)

    def _check_user_exist(self, username):
        user = UserModel.objects.filter(username=username)
        if user:
            raise_400(USER_ALREADY_PRESENT)


    def post(self, request):
        serializer  = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        self._check_user_exist(username)

        user_obj = UserModel.register(username=username, password=password)
        payload = {"id": user_obj.id, "username": user_obj.username}
        return Response(status=200, data=payload)

class LoginAPIView(APIView):

    """
    Login API
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def get_serializer(self, *args, **kwargs):
        """Return view serializer class"""
        return self.serializer_class(*args, **kwargs)

    def _check_user(self, username):
        try:
            user = UserModel.objects.get(username=username)
            if not user:
                raise_400(USER_NOT_EXIST)
        except Exception as e:
            raise_400(USER_NOT_EXIST)
        return user
    
    def generate_jwt_token(self, data):
        data['created_at'] = str(datetime.utcnow())

        return 'JWT {}'.format(jwt.encode(data,settings.JWT_SECRET_KEY, algorithm='HS256'))


    def post(self, request):
        serializer  = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = self._check_user(username)

        verified_check = UserModel.verify_password(user.password, password, username)

        if verified_check:
            token = self.generate_jwt_token({"username": username, "id": str(user.id) })
        else:
            return Response(status=403, data={"message": INVALID_LOGIN})
        return Response(status=200, data={"token":token})

class LogoutAPIView(APIView):

    """
    Logiout API
    """

    permission_classes = [IsAuthenticated, IsTokenValid]
    # serializer_class = LoginSerializer

    # def get_serializer(self, *args, **kwargs):
    #     """Return view serializer class"""
    #     return self.serializer_class(*args, **kwargs)


    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        user_id = request.user.user_id
        user_obj = UserModel(id=user_id)
        blt_obj = BlackListedToken(token=token, user=user_obj)
        blt_obj.save()
        return Response(status=200, data={"messge": "logout successfully"})
        # serializer  = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        # username = serializer.validated_data['username']
        # password = serializer.validated_data['password']

        # user = self._check_user(username)

        # verified_check = UserModel.verify_password(user.password, password, username)

        # if verified_check:
        #     token = self.generate_jwt_token({"username": username, "id": str(user.id) })
        # else:
        #     return Response(status=403, data={"message": INVALID_LOGIN})
        # return Response(status=200, data={"token":token})

