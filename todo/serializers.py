from rest_framework import serializers
from todo.models import TasksModel, ProfilePictureModel, GroupModel, MembershipModel, JoinGroupRequestModel
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


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = ['name', 'about', 'public']


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = '__all__'


class Membership:
    pass


class GroupJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipModel
        fields = ['user', 'inviter', 'is_approved']
        read_only_fields = ['user']


class GroupJoinRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinGroupRequestModel
        fields = '__all__'
        read_only_fields = ('invited', 'invitor', 'group', 'sent_at', 'request_to_join', 'invitation')


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel
        fields = ["task", "descriptions", "date", "durations", "done"]


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel

        fields = '__all__'
