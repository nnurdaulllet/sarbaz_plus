'''from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from .models import *
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail

class CreateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
           model = Applications
           fields = '__all__'

           read_only_fields = ('date_time',)

class ApplicationFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFiles
        fields = ['file']

class CreateApplicationSerializer(serializers.ModelSerializer):
    files = ApplicationFilesSerializer(many=True, required=False)

    class Meta:
        model = Applications
        fields = ['user', 'catalog', 'education_type', 'is_work_exp', 'work_describe', 'is_deferment', 'deferment', 'status', 'files']

    def create(self, validated_data):
        files_data = self.context['request'].FILES.getlist('files')
        application = Applications.objects.create(**validated_data)
        for file in files_data:
            ApplicationFiles.objects.create(application=application, file=file)
        return application



class DefermentFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDeferment
        fields = ['file']


class CreateApplicationSerializer(serializers.ModelSerializer):
    files = ApplicationFilesSerializer(many=True, required=False)
    deferment = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ApplicationDeferment.objects.all(),
        required=False
    )

    class Meta:
        model = Applications
        fields = ['user', 'catalog', 'education_type', 'is_work_exp',
                  'work_describe', 'is_deferment', 'deferment', 'files']

    def validate(self, attrs):
        is_deferment = attrs.get('is_deferment')

        if isinstance(is_deferment, str):
            is_deferment = is_deferment.lower() == 'true'

        if not is_deferment and attrs.get('deferment'):
            raise serializers.ValidationError({
                "deferment": "Это поле должно быть пустым, если is_deferment = false."
            })

        return attrs

    def create(self, validated_data):
        files_data = self.context['request'].FILES.getlist('files')
        deferments = validated_data.pop('deferment', [])
        application = Applications.objects.create(**validated_data)

        if deferments:
            application.deferment.set(deferments)

        for file in files_data:
            ApplicationFiles.objects.create(application=application, file=file)

        return application
'''

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Applications, ApplicationFiles, ApplicationDeferment


class ApplicationDefermentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDeferment
        fields = ['file']


class ApplicationFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationFiles
        fields = ['file']


class CreateApplicationSerializer(serializers.ModelSerializer):
    files = ApplicationFilesSerializer(many=True, required=False)
    deferment = ApplicationDefermentSerializer(many=True, required=False)

    class Meta:
        model = Applications
        fields = [
            'user', 'catalog', 'education_type', 'is_work_exp',
            'work_describe', 'is_deferment', 'deferment', 'files', 'status'
        ]

    def validate(self, attrs):
        is_deferment = attrs.get('is_deferment')

        # Приведение строки к булевому значению, если пришло из form-data
        if isinstance(is_deferment, str):
            is_deferment = is_deferment.lower() == 'true'

        if not is_deferment and attrs.get('deferment'):
            raise serializers.ValidationError({
                "deferment": "Это поле должно быть пустым, если is_deferment = false."
            })

        return attrs

    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        deferments_data = validated_data.pop('deferment', [])

        application = Applications.objects.create(**validated_data)

        # Сохраняем файлы заявки
        for file_data in files_data:
            file_instance = ApplicationFiles.objects.create(application=application, **file_data)
            application.files.add(file_instance)

        # Сохраняем файлы отсрочек
        for deferment_data in deferments_data:
            deferment_instance = ApplicationDeferment.objects.create(application=application, **deferment_data)
            application.deferment.add(deferment_instance)

        return application

