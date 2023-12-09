from django.db import models
from django.contrib.auth.models import User


class TasksModel(models.Model):
    task = models.CharField(max_length=255)
    descriptions = models.TextField(null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    durations = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False, blank=True)
    about = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.task


class ProfilePictureModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,upload_to='profile_pictures')


class GroupModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    public = models.BooleanField(default=False)
    about = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, editable=False)
    members = models.ManyToManyField(
        User,
        through="MembershipModel",
        through_fields=("group", "user"),
        related_name="group",
    )


class MembershipModel(models.Model):
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="membership_invites",
        null=True
    )


class FriendshipModel(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship2')
    created_at = models.DateField(auto_now=True)


class FriendRequestModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_receiver')
    status = models.CharField(default="Pending", editable=False)
