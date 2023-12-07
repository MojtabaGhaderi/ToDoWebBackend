from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate, login

from .serializers import TasksSerializer, AboutSerializer, ProfileUserSerializer, UserSerializer
from .models import TasksModel


class LoginAPIView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request.user)
            return Response({'detail': 'authentication successfull.'})
        return Response({'detail': 'invalid'}, status=status.HTTP_401_UNAUTHORIZED)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TasksSerializer


class TasklistView(generics.ListAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer
