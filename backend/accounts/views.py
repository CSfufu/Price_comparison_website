from django.shortcuts import render

# Create your views here.
# accounts/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

# accounts/views.py


class UserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'username': user.username,
            'email': user.email,
            # 添加其他需要的字段
        }
        return Response(data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # 从请求中获取 refresh token
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # 将 refresh token 添加到黑名单
            token.blacklist()
            return Response({"detail": "成功登出"}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "未提供 refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "无效的 token"}, status=status.HTTP_400_BAD_REQUEST)