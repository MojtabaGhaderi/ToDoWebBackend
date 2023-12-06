from rest_framework import generics
from .serializers import TasksSerializer, AboutSerializer
from .models import TasksModel


class TasklistView(generics.ListCreateAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = TasksSerializer


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = AboutSerializer
