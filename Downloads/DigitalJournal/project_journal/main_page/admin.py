from django.contrib import admin
from .models import Student, UserProfile

# Проверяем, зарегистрирована ли модель Student
if not admin.site.is_registered(Student):
    @admin.register(Student)
    class StudentAdmin(admin.ModelAdmin):
        list_display = ('id', 'last_name', 'first_name', 'patronymic', 'grade', 'course_completion')
        list_filter = ('grade', 'course_completion')
        search_fields = ('last_name', 'first_name', 'patronymic')

# Проверяем, зарегистрирована ли модель UserProfile
if not admin.site.is_registered(UserProfile):
    @admin.register(UserProfile)
    class UserProfileAdmin(admin.ModelAdmin):
        list_display = ('user', 'role')
        list_filter = ('role',)
        search_fields = ('user__username',)
