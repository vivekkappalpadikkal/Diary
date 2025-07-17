from django.contrib import admin
from .models import Quote,DiaryEntry,UserProfile, Goal, TodoList



admin.site.register(Quote)
admin.site.register(DiaryEntry)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')  # Display user and profile picture in the list view
    list_filter = ('user',)  # Filter by user in the admin interface
    search_fields = ('user__username',)  # Search by username in the admin interface

admin.site.register(UserProfile, UserProfileAdmin)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'short_term_goal', 'long_term_goal', 'goal_target_date']
    search_fields = ['short_term_goal', 'long_term_goal', 'user__username']

@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ['user', 'tasks']
    search_fields = ['user__username']
    list_filter = ['user']
