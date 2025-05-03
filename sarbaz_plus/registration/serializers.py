# users/serializers.py (необязательный)

from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import EmailVerification
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail

User = get_user_model()

'''class PersonRegisterSerializer(UserCreateSerializer):
    re_password = serializers.CharField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'iin', 'email', 'password', 're_password',
            'first_name', 'last_name', 'middle_name',
            'date_of_birthday', 'address', "phone_number"
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')  # Удаляем, чтобы не мешал при создании
        user = User.objects.create_user(**validated_data)
        return user
'''


class PersonRegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)
    verification_code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'iin', 'email', 'password', 're_password',
            'first_name', 'last_name', 'middle_name',
            'date_of_birthday', 'address', 'phone_number',
            'verification_code'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise ValidationError("Пароли не совпадают.")

        email = attrs.get('email')
        code = attrs.get('verification_code')

        try:
            record = EmailVerification.objects.get(email=email)
        except EmailVerification.DoesNotExist:
            raise ValidationError("Код подтверждения не найден.")

        if not record.is_valid():
            raise ValidationError("Код просрочен.")

        if record.code != code:
            raise ValidationError("Неверный код подтверждения.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')
        validated_data.pop('verification_code')
        user = User.objects.create_user(**validated_data)
        return user



class PersonGetSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id', 'iin', 'email',
            'first_name', 'last_name', 'middle_name',
            'date_of_birthday', 'address'
        )

# registration/serializers.py



class LoginSerializer(serializers.Serializer):
    iin = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        iin = data.get('iin')
        password = data.get('password')

        user = authenticate(request=self.context.get('request'), iin=iin, password=password)

        if not user:
            raise AuthenticationFailed("Неверный IIN или пароль")

        if not user.is_active:
            raise AuthenticationFailed("Пользователь деактивирован")

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'iin': user.iin,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }






