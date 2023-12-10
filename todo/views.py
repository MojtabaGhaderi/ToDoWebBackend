from rest_framework import generics
from rest_framework.authentication import SessionAuthentication

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login

from .serializers import (TasksSerializer, AboutSerializer,
                          ProfileUserSerializer, UserSerializer,
                          GroupCreateSerializer, GroupDetailSerializer, UserProfileDetailSerializer)
from .models import TasksModel, User, GroupModel, MembershipModel

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
