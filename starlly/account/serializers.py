from djoser.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for User Model CRUD """
    class Meta:
        model = get_user_model()
        fields = (
            'id','first_name','last_name','email', 'password','is_staff',
            'is_active', 'is_superuser')
        extra_kwargs = {
            'password': {'write_only': True}
            }

    def create(self, validated_data):
        """ cutom create to handle password """
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        user.set_password(make_password(password))
        user.save()
        return user


class TokenSerializer(serializers.ModelSerializer):
    """ Serialier for generating token and returning response while Login"""
    auth_token = serializers.CharField(source="key")
    user = UserSerializer()
    class Meta:
        model = settings.TOKEN_MODEL
        fields = ("auth_token", "user")
