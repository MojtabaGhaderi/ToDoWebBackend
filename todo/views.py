from django.db.models import Q
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login

from rest_framework.exceptions import ValidationError
from .serializers import (TasksSerializer, AboutSerializer,
                          ProfileUserSerializer, UserSerializer,
                          GroupCreateSerializer, GroupDetailSerializer, FriendRequestSerializer,
                          UserProfileDetailSerializer, FriendRequestResponseSerializer, FriendshipSerializer,
                          TaskGroupSerializer, GroupJoinRequestsSerializer, GroupJoinSerializer)

from .models import TasksModel, User, GroupModel, MembershipModel, FriendRequestModel, FriendshipModel

from .models import TasksModel, User, GroupModel, MembershipModel, JoinGroupRequestModel



# /////
# user related views:
# ////


class LoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({'detail': 'authentication successfull.'})
        return Response({'detail': 'invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileEditView(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer

# ////////#
# Friend related views here:
# ///////#


class FriendRequestCreate(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):

        # I'm not sure that this works...

        receiver_id = kwargs['profile_id']
        receiver = User.objects.get(id=receiver_id)
        serializer = self.get_serializer(data=request.data, context={'receiver': receiver})
        serializer.is_valid(raise_exeption=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FriendRequestResponse(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendRequestResponseSerializer
    queryset = FriendRequestModel.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save()
        status = instance.status

        if status == 'P':
            receiver = instance.receiver
            sender = instance.sender
            friendship = FriendshipModel.objects.create(user1=sender, user2=receiver)
            instance.delete()
        elif status == 'N':
            instance.delete()


class FriendListView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id

        return FriendshipModel.objects.filter(user1=user_id) | FriendshipModel.objects.filter(user2=user_id)


class FriendListEdit(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id

        return FriendshipModel.objects.filter(user1=user_id) | FriendshipModel.objects.filter(user2=user_id)

# ////////#
# Group related views here:
# ///////#


class GroupCreateView(generics.CreateAPIView):
    serializer_class = GroupCreateSerializer


class GroupDetailView(generics.RetrieveAPIView):
    serializer_class = GroupDetailSerializer


class GroupJoinView(generics.CreateAPIView):
    serializer_class = GroupJoinSerializer

    def post(self, request, *args, **kwargs):
        group_id = self.request.get('group_id')
        group = GroupModel.objects.get(id=group_id)
        user = request.user

        if group.public:
            membership = MembershipModel(user=user, group=group)
            membership.save()
            return Response({'detail': 'you are now a member of this group.'})

        else:
            join_group_request = JoinGroupRequestModel(invited=user, group=group, request_to_join=True)
            join_group_request.save()
            return Response({'detail': 'your join request has been sent and now is pending.'})


class GroupSendInvitationView(generics.CreateAPIView):
    serializer_class = GroupJoinRequestsSerializer

    def post(self, request, *args, **kwargs):
        group_id = self.request.get('group_id')
        group = GroupModel.objects.get(id=group_id)

        user_id = self.request.get('user_id')
        user = User.objects.get(id=user_id)

        invitor = request.user

        invitation = JoinGroupRequestModel(invited=user, group=group, invitor=invitor, invitation=True)
        invitation.save()


class GroupJoinRequestResponse(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupJoinRequestsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return JoinGroupRequestModel.objects.filter(group_id=group_id)

    def perform_update(self, serializer):
        accepted = serializer.validated_data.get('accepted', None)
        group = serializer.validated_data.get('group', None)
        invited = serializer.validated_data.get('invited', None)
        if accepted is not None and accepted:
            membership = MembershipModel(user=invited, group=group)
            membership.save()
            join_request = JoinGroupRequestModel.objects.filter(group=group, invited=invited)
            join_request.delete()
        elif accepted is False:
            join_request = JoinGroupRequestModel.objects.filter(group=group, invited=invited)
            join_request.delete()


class GroupJoinInvitationResponse(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupJoinRequestsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return JoinGroupRequestModel.objects.filter(invited=user)

    def perform_update(self, serializer):
        group = serializer.validated_data.get('group', None)
        invited = serializer.validated_data.get('invited', None)
        invitor = serializer.validated_data.get('invitor', None)
        accepted = serializer.validated_data.get('accepted', None)

        if accepted is not None and accepted:
            membership = MembershipModel(user=invited, group=group, invitor=invitor)
            membership.save()
            join_request = JoinGroupRequestModel.objects.filter(group=group, invited=invited, invitor=invitor)
            join_request.delete()
        elif accepted is False:
            join_request = JoinGroupRequestModel.objects.filter(group=group, invited=invited, invitor=invitor)
            join_request.delete()






class GroupUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = GroupDetailSerializer


@api_view(['GET'])
def group_router(request, *args, **kwargs):
    group = GroupModel.objects.get(pk=kwargs['pk'])
    if group.creator == request.user:
        return GroupUpdateView.as_view()(request, *args, **kwargs)
    else:
        return GroupDetailView.as_view()(request, *args, **kwargs)

# ////////#
# Tasks here:
# ///////#


class TaskCreateView(generics.CreateAPIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = TasksSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GroupTaskCreate(generics.CreateAPIView):
    # authentication needed
    serializer_class = TaskGroupSerializer

    def perform_create(self, serializer):
        group_id = self.request.data.get('group_id')
        group = GroupModel.objects.get(id=group_id)
        serializer.save(in_group=group, status='G')


class TasklistView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer


# //////////
# Feed views from here:
# ////

class PublicTasksViews(generics.ListAPIView):
    queryset = TasksModel.objects.filter(status='P')
    serializer_class = AboutSerializer


from django.db.models import Q


class FriendTasksView(generics.ListAPIView):
    serializer_class = AboutSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        friends = FriendshipModel.objects.filter(Q(user1=user_id) | Q(user2=user_id))
        friend_ids = [friend.user1_id if friend.user2_id == user_id else friend.user2_id for friend in friends]
        return TasksModel.objects.filter(creator_id__in=friend_ids, status='F')





