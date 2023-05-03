from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from .models import MyTopic,UserProfile
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount

def user_logged_in_handler(sender, request, user, **kwargs):
    if user.is_superuser or user.is_staff:
        # user is admin or staff, so let's update the status of topic requests
        for topic_request in MyTopic.objects.filter(status='Chờ tiếp nhận'):
            topic_request.status = 'Đã tiếp nhận'
            topic_request.start_time_request = timezone.now()
            topic_request.save()

@receiver(post_save, sender=MyTopic)
def update_topic_request_status(sender, instance, **kwargs):
    if instance.start_time_request is not None:
        instance.status = 'Đã tiếp nhận'
        instance.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



@receiver(post_save, sender=User)
def remove_staff_permission(sender, instance, created, **kwargs):
    if created:
        social_account = SocialAccount.objects.filter(user=instance).first()
        if social_account and social_account.provider == 'microsoft':
            instance.is_staff = False
            instance.save()