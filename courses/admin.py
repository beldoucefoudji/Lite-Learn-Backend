from django.contrib import admin
from .models import Course, Lesson, Quiz, Question, Enrollment, Progress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)} 

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',) 

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Enrollment)
admin.site.register(Progress)