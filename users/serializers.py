from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=Profile.USER_TYPE_CHOICES)


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        user = User.objects.create(**validated_data)
        user.profile.user_type = user_type
        user.profile.save()
        return user
