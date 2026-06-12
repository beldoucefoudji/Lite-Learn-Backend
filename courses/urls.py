from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, LessonViewSet, EnrollmentViewSet, ProgressViewSet,
    RegisterView, LoginView,
    UserProfileView, ProfileAvatarView, ChangePasswordView,
    AdminUserViewSet, AdminCourseViewSet, AdminLessonViewSet
)


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'progress', ProgressViewSet, basename='progress')
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')
router.register(r'admin/courses', AdminCourseViewSet, basename='admin-course')
router.register(r'admin/lessons', AdminLessonViewSet, basename='admin-lesson')

urlpatterns = [
    
    path('', include(router.urls)),
    
    
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', UserProfileView.as_view(), name='user-profile'),
    path('auth/profile/avatar/', ProfileAvatarView.as_view(), name='profile-avatar'),
    path('auth/password/', ChangePasswordView.as_view(), name='change-password'),
]
