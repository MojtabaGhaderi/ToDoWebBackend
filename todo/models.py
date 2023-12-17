from django.db import models
from django.contrib.auth.models import User


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


class TasksModel(models.Model):
    task = models.CharField(max_length=255)
    descriptions = models.TextField(null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    durations = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False, blank=True)
    about = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    in_group = models.ForeignKey(GroupModel, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)

    status_choices = [
        ('S', 'Private'),
        ('F', 'Friends'),
        # ('G', 'Groups'),
        ('P', 'Public')
    ]
    status = models.CharField(max_length=1, choices=status_choices, default='F')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.task


class ProfilePictureModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True, upload_to='profile_pictures')
    about_me = models.TextField(blank=True)
    points = models.IntegerField(default=0, editable=False)


class MembershipModel(models.Model):
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    # is_approved = models.BooleanField(default=False)
    invitor = models.ForeignKey(
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

    choices = [
        ("P", "pending"),
        ("Y", "accepted"),
        ("N", "denied")
    ]
    status = models.CharField(max_length=1, default="Pending", choices=choices , editable=False)


class JoinGroupRequestModel(models.Model):
    invited = models.OneToOneField(User, on_delete=models.CASCADE)
    invitor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='invitor', null=True)
    group = models.OneToOneField(GroupModel, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    request_to_join = models.BooleanField(default=False, editable=False)
    invitation = models.BooleanField(default=False, editable=False)
    accepted = models.BooleanField(default=None)

