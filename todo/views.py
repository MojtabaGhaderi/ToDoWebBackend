from rest_framework import generics
from .serializers import TasksSerializer, AboutSerializer
from .models import TasksModel


class TaskCreateView(generics.CreateAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = TasksSerializer


class TasklistView(generics.ListAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer
