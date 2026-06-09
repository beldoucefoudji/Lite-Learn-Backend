from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Course, Lesson, Enrollment, Progress, LearnerProfile
from .serializers import (
    CourseListSerializer, CourseDetailSerializer, EnrollmentSerializer, 
    LessonSerializer, ProgressSerializer, RegisterSerializer,
    UserAccountSerializer, ProfileAvatarSerializer, AdminUserSerializer,
    AdminCourseSerializer, AdminLessonSerializer
)


def user_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
    }

# ==========================================
# USER REGISTRATION VIEW
# ==========================================
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create token for the new user
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "User created successfully!",
                    "token": token.key,
                    "user": {
                        **user_payload(user),
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ==========================================
# NEW: USER LOGIN VIEW (TOKEN AUTHENTICATION)
# ==========================================
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Authenticate user with username and password.
        Returns auth token for subsequent requests.
        """
        username = request.data.get('username', '').strip()
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"detail": "Please provide both username and password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if '@' in username:
            matching_user = User.objects.filter(email__iexact=username).first()
            if matching_user:
                username = matching_user.username

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Get or create token for this user
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user": {
                    **user_payload(user),
                }
            },
            status=status.HTTP_200_OK
        )


# ==========================================
# NEW: USER PROFILE VIEW
# ==========================================
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get the current logged-in user's profile"""
        user = request.user
        
        # Calculate user progress and stats
        enrollments = Enrollment.objects.filter(user=user)
        total_courses = enrollments.count()
        
        # Calculate progress percentage
        total_lessons = 0
        completed_lessons = 0
        for enrollment in enrollments:
            course_lessons = Lesson.objects.filter(course=enrollment.course).count()
            total_lessons += course_lessons
            
            progress_count = Progress.objects.filter(
                enrollment=enrollment,
                is_completed=True
            ).count()
            completed_lessons += progress_count
        
        progress_percentage = (
            (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        )

        todays_progress = Progress.objects.filter(
            enrollment__user=user,
            last_accessed__date=timezone.now().date()
        ).count()

        points_earned = completed_lessons * 10

        learner_profile, _ = LearnerProfile.objects.get_or_create(user=user)
        account = UserAccountSerializer(user, context={'request': request}).data
        skills = sorted({
            enrollment.course.get_category_display()
            for enrollment in enrollments
            if Progress.objects.filter(enrollment=enrollment, is_completed=True).exists()
        })
        completed_courses = sum(
            1 for enrollment in enrollments
            if enrollment.course.lessons.exists()
            and Progress.objects.filter(
                enrollment=enrollment,
                is_completed=True,
            ).count() == enrollment.course.lessons.count()
        )

        return Response({
                **account,
                "id": user.id,
                "total_courses": total_courses,
                "completed_lessons": completed_lessons,
                "total_lessons": total_lessons,
                "progress_percentage": round(progress_percentage, 2),
                "day_streak": 1 if todays_progress > 0 else 0,
                "points_earned": points_earned,
                "learning_hours": round(completed_lessons * 0.75, 1),
                "skills": skills,
                "completed_courses": completed_courses,
                "linked_accounts": {
                    "github": False,
                },
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            })

    def patch(self, request):
        LearnerProfile.objects.get_or_create(user=request.user)
        serializer = UserAccountSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileAvatarView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile, _ = LearnerProfile.objects.get_or_create(user=request.user)
        serializer = ProfileAvatarSerializer(
            profile,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        profile, _ = LearnerProfile.objects.get_or_create(user=request.user)
        if profile.avatar:
            profile.avatar.delete(save=False)
        profile.avatar = ''
        profile.avatar_url = ''
        profile.save(update_fields=['avatar', 'avatar_url'])
        return Response({'avatar_url': ''})


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('current_password', '')
        new_password = request.data.get('new_password', '')
        user = request.user

        if user.has_usable_password() and not user.check_password(current_password):
            return Response(
                {"current_password": ["Current password is incorrect."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            from django.contrib.auth.password_validation import validate_password
            validate_password(new_password, user=user)
        except Exception as error:
            return Response(
                {"new_password": list(error.messages)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save(update_fields=['password'])
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return Response({"detail": "Password updated.", "token": token.key})

# ==========================================
# COURSE VIEWSET
# ==========================================
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Exposes all courses publicly for browsing (GET requests), 
    ReadOnly because students don't create courses; only Admins do.
    """
    queryset = Course.objects.prefetch_related('lessons', 'quizzes__questions')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

# ==========================================
# LESSON VIEWSET
# ==========================================
class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.select_related('course')
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

# ==========================================
# ENROLLMENT VIEWSET
# ==========================================
class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    A student should only see their own enrollments.
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only returns enrollments belonging to the logged-in user
        return Enrollment.objects.filter(
            user=self.request.user,
        ).select_related('course').prefetch_related(
            'course__lessons',
            'progress_set',
        )

    def perform_create(self, serializer):
        # Automatically set the user to the logged-in user when enrolling
        serializer.save(user=self.request.user)

# ==========================================
# NEW: PROGRESS VIEWSET
# ==========================================
class ProgressViewSet(viewsets.ModelViewSet):
    """
    Track lesson completion and update progress.
    """
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show progress for enrollments the user owns
        return Progress.objects.filter(
            enrollment__user=self.request.user,
        ).select_related(
            'enrollment__course',
            'lesson',
        )


class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(
                {'detail': 'You cannot delete your own administrator account.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)


class AdminCourseViewSet(viewsets.ModelViewSet):
    serializer_class = AdminCourseSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Course.objects.all().prefetch_related('lessons').order_by('title')


class AdminLessonViewSet(viewsets.ModelViewSet):
    serializer_class = AdminLessonSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Lesson.objects.select_related('course').order_by(
        'course__title', 'order'
    )
