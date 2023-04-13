from django.contrib import admin
from .models import UserProfile,MyTopic,Topic,CustomUser,CustomUserManager,Article

admin.site.register(UserProfile)

@admin.register(MyTopic)
class MyTopicAdmin(admin.ModelAdmin):
    list_display = ('topic','status','name')
    search_fields = ('topic','description')

admin.site.register(Topic)
admin.site.register(CustomUser)
admin.site.register(Article)