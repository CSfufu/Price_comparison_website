from rest_framework import serializers
from .models import Customer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = Customer
        fields = ('username', 'password', 'email')

    def validate_username(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("用户名长度必须至少为6个字符。")
        return value

    def validate(self, data):
        if Customer.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("用户名已存在。")
        if Customer.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("邮箱已被注册。")
        return data

    def create(self, validated_data):
        user = Customer.objects.create_user(**validated_data)
        return user
