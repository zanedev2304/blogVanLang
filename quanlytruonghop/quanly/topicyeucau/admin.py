from django.contrib import admin
from .models import UserProfile,MyTopic,Topic,CustomUser,CustomUserManager

admin.site.register(UserProfile)
admin.site.register(MyTopic)
admin.site.register(Topic)
admin.site.register(CustomUser)
