from django.urls import path
from todo import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('tasks/', views.TasklistView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)