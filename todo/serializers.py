from rest_framework import serializers
from todo.models import TasksModel


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel
        fields = ["task", "descriptions", "date", "durations", "done"]


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModel

        fields = '__all__'
