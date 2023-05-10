from django.contrib import admin
from .models import UserProfile,MyTopic,Topic,CustomUser,CustomUserManager,Article,Category,Rating,Knowledge

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('topic','score')

@admin.register(MyTopic)
class MyTopicAdmin(admin.ModelAdmin):
    list_display = ('topic','status','employee')
    search_fields = ('topic','description')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title','category','author')
    date_hierarchy = 'start_time'

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, "Đã xoá thành công các bài viết đã chọn.")
    delete_selected.short_description = "Xoá bài viết đã chọn"

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'student_id', 'course','role')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ('category','content')



admin.site.register(UserProfile, UserProfileAdmin)


admin.site.register(CustomUser)
admin.site.register(Article)