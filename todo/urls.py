from django.urls import path
from todo import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('tasks/', views.TasklistView.as_view(), name='tasks'),
    path('tasks/create/',views.TaskCreateView.as_view(), name='create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),

    path('groups/<int:pk>/', views.group_router, name='group_router'),

    path('profile/<int:pk>',views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile/', views.UserProfileEditView.as_view(), name='profile'),

    path('friends', views.FriendListView.as_view(), name='friend_list'),
    path('friends/edit', views.FriendListEdit.as_view(), name='Friend_edit'),

    path('login/', views.LoginAPIView.as_view(), name='login'),

    path('signup/', views.UserCreateView.as_view(), name='signup'),

    path('public-tasks/', views.PublicTasksViews.as_view(), name='public_tasks'),

]


urlpatterns = format_suffix_patterns(urlpatterns)