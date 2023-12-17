from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from todo.models import TasksModel
from django.contrib.auth.models import User


@receiver(pre_save, sender=TasksModel)
def update_user_points(sender, instance, **kwargs):
    user = instance.creator
    if instance.pk:
        original_task = TasksModel.objects.get(pk=instance.pk)

        if original_task.done != instance.done:

            if instance.done:
                user.points += 100
            else:
                user.points -= 100
            user.save()

    elif instance.done:
        user.points += 100
        user.save()
