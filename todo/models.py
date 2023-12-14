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
        related_name= 'members',
        through="MembershipModel",
        through_fields=("group", "user"),
    )


class MembershipModel(models.Model):
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="membership_invites",
        null=True
    )


class JoinGroupRequestModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.OneToOneField(GroupModel, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    request_to_join = models.BooleanField(default=False, editable=False)
    invitation = models.BooleanField(default=False, editable=False)
