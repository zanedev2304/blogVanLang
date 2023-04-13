from django.contrib import admin
from .models import UserProfile,MyTopic,Topic,CustomUser,CustomUserManager,Article

admin.site.register(UserProfile)

@admin.register(MyTopic)
class MyTopicAdmin(admin.ModelAdmin):
    list_display = ('topic','status','name')
    search_fields = ('topic','description')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author')
    date_hierarchy = 'start_time'
    search_fields = ('slug',)

admin.site.register(CustomUser)
admin.site.register(Article)