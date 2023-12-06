from rest_framework import serializers
from todo.models import TasksModel


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel
        fields = "__all__"
