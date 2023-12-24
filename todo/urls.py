from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from todo import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('tasks/', views.TasklistView.as_view(), name='tasks'),  # Fine. But this is going to be deleted.
    path('tasks/create/', views.TaskCreateView.as_view(), name='create'),  # Fine.
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),  # Fine.

    path('group-create', views.GroupCreateView.as_view(), name='group-create'),  # Fine.
    path('group-join', views.GroupJoinView.as_view(), name='group-join'),  # Fine.
    path('group/<int:pk>/update', views.GroupUpdateView.as_view(), name='group-update'),  # Fine
    path('group/<int:pk>/detail', views.GroupDetailView.as_view(), name='group-detail'),  # Fine
    path('group-send-invite', views.GroupSendInvitationView.as_view(), name='group-send-invite'),  # Fine.

    path('group/invitation', views.GroupInvitationListView.as_view(), name='group_invitation'),  # Fine.
    path('group/invitation-response/<int:pk>/', views.GroupJoinInvitationResponse.as_view(),
         name='group_invitation-response'),  # Fine.
    path('group-join-requests/<int:pk>/', views.GroupJoinRequests.as_view(), name='group_join_request'),
    path('group-join-response/<int:pk>', views.GroupJoinRequestResponse.as_view(), name='group-join-response'),
    path('mygroups', views.UserGroupListView.as_view(), name='user_groups'),
    path('grouptest/', views.JoinRequestTest.as_view(), name='grouptest'),  # for test////////////

    path('profile/<int:pk>', views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile/', views.UserProfileEditView.as_view(), name='profile'),

    path('friends', views.FriendListView.as_view(), name='friend_list'),
    path('friend-request/', views.FriendRequestCreate.as_view(), name='friend_request'),
    path('friend-request-response/<int:pk>/', views.FriendRequestResponse.as_view(), name='friend_request_response'),
    path('friends/edit/<int:pk>/', views.FriendListEdit.as_view(), name='Friend_edit'),

    path('login/', views.LoginAPIView.as_view(), name='login'),  # Fine.
    path('logout/', views.LogoutView.as_view(), name='logout'),  # fine.

    path('signup/', views.UserCreateView.as_view(), name='signup'),

    path('public-tasks/', views.PublicTaskListView.as_view(), name='public_tasks'),
    path('friends-tasks/', views.FriendTaskListView.as_view(), name='friends_tasks'),
    path('group-tasks', views.GroupTaskListView.as_view(), name='group-tasks'),
    path('group/<int:pk>/tasks/create', views.GroupTaskCreate.as_view(), name="group_task_create"),



]


urlpatterns = format_suffix_patterns(urlpatterns)