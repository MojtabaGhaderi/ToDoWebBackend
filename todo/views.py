from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login

from .serializers import (TasksSerializer, AboutSerializer,
                          ProfileUserSerializer, UserSerializer,
                          GroupCreateSerializer, GroupDetailSerializer, FriendRequestSerializer,
                          UserProfileDetailSerializer, FriendRequestResponseSerializer, FriendshipSerializer)

from .models import TasksModel, User, GroupModel, MembershipModel, FriendRequestModel, FriendshipModel


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

# ////////#
# Group related views here:
# ///////#


class GroupCreateView(generics.CreateAPIView):
    serializer_class = GroupCreateSerializer


class GroupDetailView(generics.RetrieveAPIView):
    serializer_class = GroupDetailSerializer


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


class TasklistView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer
