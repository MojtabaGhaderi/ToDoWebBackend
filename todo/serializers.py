from rest_framework import serializers
from todo.models import TasksModel, ProfilePictureModel, GroupModel, FriendRequestModel
from django.contrib.auth.models import User


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePictureModel
        fields = ['profile_pic']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    profile_picture = ProfileUserSerializer()

    class Meta:
        model = User
        fields = ['username', 'profile_picture']


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


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequestModel
        fields = ['receiver']
        read_only_fields = ['receiver']

    def create(self, validated_data):
        sender = self.context['request'].user
        receiver = self.context['receiver']
        validated_data['sender'] = sender
        validated_data['status'] = 'Pending'
        validated_data['receiver'] = receiver
        return super().create(validated_data)


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = ['name', 'about', 'public']


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = '__all__'


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel
        fields = ["task", "descriptions", "date", "durations", "done"]


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel

        fields = '__all__'
