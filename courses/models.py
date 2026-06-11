from django.conf import settings
from django.db import models


class LearnerProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('premium', 'Premium Member'),
        ('instructor', 'Instructor'),
    ]
    THEME_CHOICES = [('light', 'Light'), ('dark', 'Dark'), ('system', 'System')]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='learner_profile', on_delete=models.CASCADE)
    bio = models.CharField(max_length=280, blank=True)
    avatar_url = models.URLField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='profile-pictures/%Y/%m/', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    course_announcements = models.BooleanField(default=True)
    deadline_reminders = models.BooleanField(default=True)
    forum_replies = models.BooleanField(default=False)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    autoplay_next_lesson = models.BooleanField(default=True)
    caption_language = models.CharField(max_length=30, default='English')

    def __str__(self):
        return f"{self.user.username} profile"


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('web_dev', 'Web Development'),
        ('programming', 'Programming'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web_dev')
    description = models.TextField()
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['course_id', 'order', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'order'],
                name='unique_lesson_order_per_course',
            ),
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_user_course_enrollment',
            ),
        ]

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

class Progress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['enrollment', 'lesson'],
                name='unique_enrollment_lesson_progress',
            ),
        ]

    def __str__(self):
        return f"{self.enrollment} - {self.lesson.title}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    passing_score = models.IntegerField(default=70)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    
    CORRECT_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES)

    def __str__(self):
        return self.question_text[:50]
    
