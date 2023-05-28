from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from .models import MyTopic,UserProfile,Topic,Rating,Article,Knowledge
from django.utils import timezone
from urllib.parse import urlparse
from django.http import request
from django.urls import reverse



#Loại bỏ quyền staff của tài khoản Microsoft
@receiver(user_logged_in)
def remove_staff_status(sender, user, request, **kwargs):
    email = user.email
    if email and (email.endswith('@outlook.com.vn') or email.endswith('@vanlanguni.vn')):
        if user.is_staff:
            user.is_staff = False
            user.save()






@receiver(post_save, sender=MyTopic)
def create_rating_for_topic(sender, instance, created, **kwargs):
    if instance.status == 'Hoàn thành':
        Rating.objects.get_or_create(topic=instance.topic)



@receiver(post_save, sender=Article)
def update_knowledge_content(sender, instance, created, **kwargs):
    if created:
        # Tìm các Knowledge có category trùng khớp với category của Article
        matching_knowledge = Knowledge.objects.filter(category=instance.category)
        
        for knowledge in matching_knowledge:
            # Thêm đường dẫn của Article vào content của Knowledge
            knowledge.content += f'<a href="{instance.get_absolute_url()}">{instance.title}</a>'
            knowledge.save()




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)






