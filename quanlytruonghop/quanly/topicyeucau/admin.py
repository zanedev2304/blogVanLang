from django.contrib import admin
from .models import UserProfile,MyTopic,Topic,CustomUser,CustomUserManager,Article



@admin.register(MyTopic)
class MyTopicAdmin(admin.ModelAdmin):
    list_display = ('topic','status','name')
    search_fields = ('topic','description')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author')
    date_hierarchy = 'start_time'
    search_fields = ('slug',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'student_id', 'course')

admin.site.register(UserProfile, UserProfileAdmin)


admin.site.register(CustomUser)
admin.site.register(Article)