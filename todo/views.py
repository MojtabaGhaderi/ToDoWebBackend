from rest_framework import generics
from .serializers import TasksSerializer, AboutSerializer, ProfileUserSerializer, UserSerializer
from .models import TasksModel


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
