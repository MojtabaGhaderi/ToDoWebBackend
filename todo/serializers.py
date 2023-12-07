from rest_framework import serializers
from todo.models import TasksModel, ProfilePictureModel
from django.contrib.auth.models import User


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePictureModel
        fields = ['profile_pic']


class UserSerializer(serializers.ModelSerializer):
    profile_pic = ProfileUserSerializer(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'profile_pic']

    def create(self, validated_data):
        profile_pic_data = validated_data.pop('profile_pic', None)
        user = User.objects.create_user(**validated_data)

        if profile_pic_data:
            ProfilePictureModel.objects.create(user=user, **profile_pic_data)
        return user


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel
        fields = ["task", "descriptions", "date", "durations", "done"]


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel

        fields = '__all__'
