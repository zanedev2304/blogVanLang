from django.contrib import admin
from .models import UserProfile,MyTopic,Topic

admin.site.register(UserProfile)
admin.site.register(MyTopic)
admin.site.register(Topic)