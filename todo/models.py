from django.db import models


class TasksModel(models.Model):
    task = models.CharField(max_length=255)
    descriptions = models.TextField(null=True, blank=True)
    date = models.DateTimeField(blank=True)
    durations = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False, blank=True)
    about = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.task

