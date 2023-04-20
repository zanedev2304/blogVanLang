from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import MyTopic

@receiver(user_logged_in, sender=User)
def user_logged_in_handler(sender, request, user, **kwargs):
    if user.is_superuser or user.is_staff:
        # user is admin or staff, so let's update the status of topic requests
        for topic_request in MyTopic.objects.filter(status='Chờ tiếp nhận'):
            topic_request.status = 'Đã tiếp nhận'
            topic_request.save()

@receiver(post_save, sender=MyTopic)
def update_topic_request_status(sender, instance, **kwargs):
    if instance.status == 'Chờ tiếp nhận' and instance.start_time_request is not None:
        instance.status = 'Đã tiếp nhận'
        instance.save()
