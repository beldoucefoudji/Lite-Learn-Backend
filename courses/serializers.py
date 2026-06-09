from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Course, Lesson, Quiz, Question, Enrollment, Progress, LearnerProfile

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # We exclude 'correct_answer' so students can't cheat by looking at the JSON!
        fields = ['id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'passing_score', 'questions']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'slug', 'content', 'video_url', 'order']


class AdminCourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lessons.count', read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'category', 'description',
            'thumbnail_url', 'lesson_count',
        ]


class AdminLessonSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'course', 'course_title', 'title', 'slug',
            'content', 'video_url', 'order',
        ]


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        min_length=8,
    )
    enrollment_count = serializers.IntegerField(
        source='enrollment_set.count',
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'is_active', 'is_staff', 'is_superuser',
            'date_joined', 'last_login', 'enrollment_count',
        ]
        read_only_fields = ['is_superuser', 'date_joined', 'last_login']

    def validate_password(self, value):
        user = self.instance or User(
            username=self.initial_data.get('username', ''),
            email=self.initial_data.get('email', ''),
        )
        try:
            validate_password(value, user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages) from error
        return value

    def validate(self, data):
        request = self.context['request']
        if self.instance == request.user:
            if data.get('is_active') is False:
                raise serializers.ValidationError(
                    {'is_active': 'You cannot block your own administrator account.'}
                )
            if data.get('is_staff') is False:
                raise serializers.ValidationError(
                    {'is_staff': 'You cannot remove your own administrator access.'}
                )
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CourseListSerializer(serializers.ModelSerializer):
    """Used for the homepage/catalog where we now also load the nested lessons!"""
    lessons = LessonSerializer(many=True, read_only=True) 

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'category', 'thumbnail_url', 'description', 'lessons'] 

class CourseDetailSerializer(serializers.ModelSerializer):
    """Used when a student clicks a course to see all lessons and quizzes"""
    lessons = LessonSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'category', 'description', 'thumbnail_url', 'lessons', 'quizzes']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_password(self, value):
        user = User(
            username=self.initial_data.get('username', ''),
            email=self.initial_data.get('email', ''),
        )
        try:
            validate_password(value, user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.messages) from error
        return value

    def create(self, validated_data):
        # This securely hashes the password before saving it to the database
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class LearnerProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = LearnerProfile
        fields = [
            'bio', 'avatar_url', 'role', 'email_notifications',
            'push_notifications', 'course_announcements', 'deadline_reminders',
            'forum_replies', 'theme', 'autoplay_next_lesson',
            'caption_language',
        ]
        read_only_fields = ['role']

    def get_avatar_url(self, instance):
        if instance.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(instance.avatar.url)
            return instance.avatar.url
        return instance.avatar_url


class ProfileAvatarSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = LearnerProfile
        fields = ['avatar', 'avatar_url']
        extra_kwargs = {'avatar': {'write_only': True, 'required': True}}

    def validate_avatar(self, image):
        if image.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Profile pictures must be 5 MB or smaller.')
        if image.content_type not in {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}:
            raise serializers.ValidationError('Use a JPG, PNG, WEBP, or GIF image.')
        return image

    def get_avatar_url(self, instance):
        if not instance.avatar:
            return ''
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(instance.avatar.url)
        return instance.avatar.url

    def update(self, instance, validated_data):
        previous_avatar = instance.avatar
        instance.avatar = validated_data['avatar']
        instance.avatar_url = ''
        instance.save(update_fields=['avatar', 'avatar_url'])
        if previous_avatar and previous_avatar.name != instance.avatar.name:
            previous_avatar.delete(save=False)
        return instance


class UserAccountSerializer(serializers.ModelSerializer):
    profile = LearnerProfileSerializer(source='learner_profile')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('learner_profile', {})
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        profile, _ = LearnerProfile.objects.get_or_create(user=instance)
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()
        return instance

class EnrollmentSerializer(serializers.ModelSerializer):
    """Enrollment with progress calculation"""
    user = serializers.ReadOnlyField(source='user.username')
    course = CourseListSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        source='course',
        queryset=Course.objects.all(),
        write_only=True,
    )
    progress_percentage = serializers.SerializerMethodField()
    current_topic_title = serializers.SerializerMethodField()
    last_accessed = serializers.SerializerMethodField()
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'course', 'course_id', 'date_enrolled',
            'progress_percentage', 'current_topic_title', 'last_accessed',
        ]
        read_only_fields = ['date_enrolled']

    def validate(self, data):
        """A user cannot enroll in the same course twice."""
        user = self.context['request'].user
        course = data.get('course') or getattr(self.instance, 'course', None)
        enrollments = Enrollment.objects.filter(user=user, course=course)

        if self.instance:
            enrollments = enrollments.exclude(pk=self.instance.pk)
        
        if course and enrollments.exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        
        return data

    def get_progress_percentage(self, instance):
        course_lessons = instance.course.lessons.count()
        if course_lessons == 0:
            return 0

        completed = instance.progress_set.filter(is_completed=True).count()
        return round((completed / course_lessons) * 100, 2)

    def get_current_topic_title(self, instance):
        completed_lesson_ids = instance.progress_set.filter(
            is_completed=True,
        ).values_list('lesson_id', flat=True)
        next_lesson = instance.course.lessons.exclude(
            id__in=completed_lesson_ids,
        ).first()
        return next_lesson.title if next_lesson else instance.course.title

    def get_last_accessed(self, instance):
        latest_progress = instance.progress_set.order_by('-last_accessed').first()
        timestamp = latest_progress.last_accessed if latest_progress else instance.date_enrolled
        return timestamp.isoformat()

class ProgressSerializer(serializers.ModelSerializer):
    """Track lesson completion"""
    progress_percentage = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Progress
        fields = [
            'id', 'enrollment', 'lesson', 'is_completed', 'last_accessed',
            'progress_percentage',
        ]
        read_only_fields = ['last_accessed']
        validators = []
    
    def validate(self, data):
        """Ensure enrollment and lesson are from the same course"""
        enrollment = data.get('enrollment') or getattr(self.instance, 'enrollment', None)
        lesson = data.get('lesson') or getattr(self.instance, 'lesson', None)
        request = self.context['request']
        
        if enrollment and enrollment.user_id != request.user.id:
            raise serializers.ValidationError(
                {"enrollment": "You can only update your own enrollment."}
            )

        if enrollment and lesson and enrollment.course_id != lesson.course_id:
            raise serializers.ValidationError(
                {"lesson": "Lesson must belong to the enrolled course."}
            )
        
        return data

    def create(self, validated_data):
        progress, _ = Progress.objects.update_or_create(
            enrollment=validated_data['enrollment'],
            lesson=validated_data['lesson'],
            defaults={'is_completed': validated_data.get('is_completed', False)},
        )
        return progress

    def get_progress_percentage(self, instance):
        lesson_count = instance.enrollment.course.lessons.count()
        if lesson_count == 0:
            return 0

        completed_count = instance.enrollment.progress_set.filter(
            is_completed=True,
        ).count()
        return round((completed_count / lesson_count) * 100, 2)
