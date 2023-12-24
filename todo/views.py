from django.db.models import Q
from django.http import HttpRequest
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth import authenticate, login, logout

from rest_framework.exceptions import ValidationError
from .serializers import (TasksSerializer, AboutSerializer,
                          ProfileUserSerializer, UserSerializer,
                          GroupCreateSerializer, GroupDetailSerializer, FriendRequestSerializer,
                          UserProfileDetailSerializer, FriendRequestResponseSerializer, FriendshipSerializer,
                          TaskGroupSerializer, GroupJoinRequestsSerializer, GroupJoinSerializer, MembershipSerializer,
                          GroupJoinTest)

from .models import TasksModel, User, GroupModel, MembershipModel, FriendRequestModel, FriendshipModel, \
    ProfilePictureModel

from .models import TasksModel, User, GroupModel, MembershipModel, JoinGroupRequestModel
from django.db.models import Q
from .permissions import IsSelf, IsSelfFriendResponse, FriendListEditPermission, IsGroupAdmin, IsGroupHead, \
    GroupJoinInvitationResponsePermission, IsInGroup, IsTaskOwner, IsGroupHeadOrAdmin


# //////////////////////////
# user related views:
# //////////////////////////


class LoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'detail': 'authentication successfull.'})
        return Response({'detail': 'invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response({'detail': 'Successfully logged out.'})


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileEditView(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsSelf]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer
    queryset = ProfilePictureModel

# ///////////////////////////
# Friend related views here:
# ///////////////////////////


class FriendRequestCreate(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):

        # I'm not sure that this works...

        receiver_id = request.data.get('id')
        receiver = User.objects.get(id=receiver_id)
        serializer = self.get_serializer(data=request.data, context={'request':request, 'receiver': receiver})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FriendRequestResponse(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSelfFriendResponse]
    serializer_class = FriendRequestResponseSerializer
    queryset = FriendRequestModel.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        status = instance.status

        if status == 'Y':
            receiver = instance.receiver
            sender = instance.sender
            friendship = FriendshipModel.objects.create(user1=sender, user2=receiver)
            instance.delete()
        elif status == 'N':
            instance.delete()
        else:
            raise ValidationError('Fuck Off! that;s not allowed!')


class FriendListView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id

        return FriendshipModel.objects.filter(user1=user_id) | FriendshipModel.objects.filter(user2=user_id)


class FriendListEdit(generics.RetrieveDestroyAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated, FriendListEditPermission]

    def get_queryset(self):
        user_id = self.request.user.id

        return FriendshipModel.objects.filter(user1=user_id) | FriendshipModel.objects.filter(user2=user_id)

# ////////////////////////////
# Group related views here:
# ///////////////////////////


class UserGroupListView(generics.ListAPIView):
    serializer_class = MembershipSerializer

    def get_queryset(self):
        user = self.request.user
        memberships = MembershipModel.objects.filter(user=user)
        groups = [membership.group for membership in memberships]

        return groups


class GroupCreateView(generics.CreateAPIView):
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save(creator=self.request.user)
        MembershipModel.objects.create(user=self.request.user, group=group)


class GroupDetailView(generics.RetrieveAPIView):
    serializer_class = GroupDetailSerializer
    queryset = GroupModel.objects.all()


class GroupJoinView(generics.CreateAPIView):
    serializer_class = GroupJoinSerializer

    def post(self, request, *args, **kwargs):
        group_id = self.request.data['group_id']
        group = GroupModel.objects.get(id=group_id)
        user = request.user

        if group.public:
            membership, created = MembershipModel.objects.get_or_create(user=user, group=group)
            if created:
                return Response({'detail': 'you are already in this group.'})
            else:
                return Response({'detail': 'you are now a member of this group.'})

        else:
            join_group_request, created = JoinGroupRequestModel.objects.get_or_create(invited=user,
                                                                                      group=group,
                                                                                      request_to_join=True)
            if created:
                return Response({'detail': 'your join request has been sent and now is pending.'})
            else:
                return Response({'detail': 'Your join request has already sent.'})


class GroupSendInvitationView(generics.CreateAPIView):
    serializer_class = GroupJoinRequestsSerializer
    permission_classes = [IsGroupAdmin, IsGroupHead]

    def post(self, request, *args, **kwargs):
        group_id = self.request.data['group_id']
        group = GroupModel.objects.get(id=group_id)

        user_id = self.request.data['user_id']
        user = User.objects.get(id=user_id)

        invitor = self.request.user

        invitation = JoinGroupRequestModel(invited=user, group=group, invitor=invitor, invitation=True)
        invitation.save()
        return Response("Invitation created successfully.", status=status.HTTP_201_CREATED)


class GroupJoinRequests(generics.ListAPIView):
    serializer_class = GroupJoinRequestsSerializer

    permission_classes = [IsGroupHead, IsGroupAdmin]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')  # Accessing the pk from URL
        group = get_object_or_404(GroupModel, id=group_id)
        return JoinGroupRequestModel.objects.filter(group=group)


class GroupJoinRequestResponse(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = GroupJoinRequestsSerializer

    permission_classes = [IsGroupHeadOrAdmin]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        id = self.kwargs.get('pk')  # Accessing the pk from URL
        return JoinGroupRequestModel.objects.filter(id=id)

    def perform_update(self, serializer):
        accepted = serializer.validated_data.get('accepted', None)
        join_request = self.get_object()
        group = join_request.group
        invited = join_request.invited
        if accepted is not None and accepted:

            membership = MembershipModel(user=invited, group=group)
            membership.save()
            join_request = JoinGroupRequestModel.objects.filter(group=group, invited=invited)
            join_request.delete()
        elif accepted is False:
            join_request = JoinGroupRequestModel.objects.filter(group=group, invited=invited)
            join_request.delete()


class GroupInvitationListView(generics.ListAPIView):
    serializer_class = GroupJoinRequestsSerializer

    def get_queryset(self):
        user = self.request.user
        return JoinGroupRequestModel.objects.filter(invited=user, invitation=True)


class GroupJoinInvitationResponse(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupJoinRequestsSerializer
    permission_classes = [GroupJoinInvitationResponsePermission]
    queryset = JoinGroupRequestModel
    # lookup_field = 'id'

    @transaction.atomic
    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        instance = serializer.save()
        group = instance.group
        accepted = instance.accepted
        invited = instance.invited
        invitor = instance.invitor

        if accepted:
            membership = MembershipModel(user=invited, group=group, invitor=invitor)
            membership.save()
            instance.delete()
        else:
            instance.delete()


class GroupUpdateView(generics.RetrieveUpdateAPIView):
    queryset = GroupModel
    serializer_class = GroupDetailSerializer
    permission_classes = [IsGroupHead, IsAuthenticated]


# //////////////////////
# Tasks here:
# //////////////////////


class TaskCreateView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TasksSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GroupTaskCreate(generics.CreateAPIView):
    permission_classes = [IsInGroup]
    serializer_class = TaskGroupSerializer

    def perform_create(self, serializer):
        group_id = self.request.data.get('group_id')
        group = GroupModel.objects.get(id=group_id)
        serializer.save(in_group=group, status='G')


class TasklistView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer
    # this view is for test and is going to be deleted


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsTaskOwner]
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer


# ///////////////////////
# Feed views from here:
# //////////////////////

class PublicTaskListView(generics.ListAPIView):
    queryset = TasksModel.objects.filter(status='P')
    serializer_class = AboutSerializer


class FriendTaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AboutSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        friends = FriendshipModel.objects.filter(Q(user1=user_id) | Q(user2=user_id))
        friend_ids = [friend.user1 if friend.user2 == user_id else friend.user2 for friend in friends]
        return TasksModel.objects.filter(creator_id__in=friend_ids, status='F')


class GroupTaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AboutSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        memberships = MembershipModel.objects.filter(user=user)
        groups = [membership.group for membership in memberships]
        return TasksModel.objects.filter(in_group__in=groups, status='G')




#this is for test///////////
class JoinRequestTest(generics.ListAPIView):
    serializer_class = GroupJoinTest
    queryset = JoinGroupRequestModel.objects.all()