from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Course, Enrollment, Lesson, Progress


@override_settings(SECURE_SSL_REDIRECT=False)
class CoursesApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='strong-password-123',
        )
        cls.other_user = User.objects.create_user(
            username='other-student',
            password='strong-password-123',
        )
        cls.admin_user = User.objects.create_superuser(
            username='platform-admin',
            email='platform-admin@example.com',
            password='admin-password-123',
        )
        cls.course = Course.objects.create(
            title='Python Basics',
            slug='python-basics',
            category='programming',
            description='Learn Python.',
        )
        cls.lesson_one = Lesson.objects.create(
            course=cls.course,
            title='Introduction',
            slug='python-introduction',
            content='Welcome',
            order=1,
        )
        cls.lesson_two = Lesson.objects.create(
            course=cls.course,
            title='Variables',
            slug='python-variables',
            content='Variables',
            order=2,
        )
        cls.other_course = Course.objects.create(
            title='Web Basics',
            slug='web-basics',
            category='web_dev',
            description='Learn web development.',
        )
        cls.other_lesson = Lesson.objects.create(
            course=cls.other_course,
            title='HTML',
            slug='html',
            content='HTML',
            order=1,
        )

    def authenticate(self, user=None):
        self.client.force_authenticate(user=user or self.user)

    def test_courses_are_public(self):
        response = self.client.get('/api/courses/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            self.course.slug,
            [course['slug'] for course in response.data],
        )

    def test_registration_returns_token(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'new-student',
                'email': 'new@example.com',
                'password': 'strong-password-123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['token'])
        self.assertTrue(User.objects.filter(username='new-student').exists())

    def test_login_returns_a_reusable_token(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.username, 'password': 'strong-password-123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], Token.objects.get(user=self.user).key)

    def test_login_accepts_an_email_address(self):
        response = self.client.post(
            '/api/auth/login/',
            {'username': self.user.email, 'password': 'strong-password-123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.user.id)

    def test_enrollment_response_contains_dashboard_fields(self):
        self.authenticate()

        response = self.client.post(
            '/api/enrollments/',
            {'course_id': self.course.id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['course']['id'], self.course.id)
        self.assertEqual(response.data['progress_percentage'], 0)
        self.assertEqual(response.data['current_topic_title'], self.lesson_one.title)
        self.assertIn('last_accessed', response.data)

    def test_duplicate_enrollment_is_rejected(self):
        Enrollment.objects.create(user=self.user, course=self.course)
        self.authenticate()

        response = self.client.post(
            '/api/enrollments/',
            {'course_id': self.course.id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            Enrollment.objects.filter(user=self.user, course=self.course).count(),
            1,
        )

    def test_users_only_see_their_own_enrollments(self):
        Enrollment.objects.create(user=self.user, course=self.course)
        Enrollment.objects.create(user=self.other_user, course=self.other_course)
        self.authenticate()

        response = self.client.get('/api/enrollments/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['course']['id'], self.course.id)

    def test_progress_creation_is_idempotent_and_returns_percentage(self):
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        self.authenticate()
        payload = {
            'enrollment': enrollment.id,
            'lesson': self.lesson_one.id,
            'is_completed': True,
        }

        first_response = self.client.post('/api/progress/', payload, format='json')
        second_response = self.client.post('/api/progress/', payload, format='json')

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.data['progress_percentage'], 50)
        self.assertEqual(
            Progress.objects.filter(
                enrollment=enrollment,
                lesson=self.lesson_one,
            ).count(),
            1,
        )

    def test_progress_cannot_use_another_users_enrollment(self):
        enrollment = Enrollment.objects.create(
            user=self.other_user,
            course=self.course,
        )
        self.authenticate()

        response = self.client.post(
            '/api/progress/',
            {
                'enrollment': enrollment.id,
                'lesson': self.lesson_one.id,
                'is_completed': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Progress.objects.exists())

    def test_progress_lesson_must_match_enrolled_course(self):
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        self.authenticate()

        response = self.client.post(
            '/api/progress/',
            {
                'enrollment': enrollment.id,
                'lesson': self.other_lesson.id,
                'is_completed': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Progress.objects.exists())

    def test_profile_aggregates_completed_lessons(self):
        enrollment = Enrollment.objects.create(user=self.user, course=self.course)
        Progress.objects.create(
            enrollment=enrollment,
            lesson=self.lesson_one,
            is_completed=True,
        )
        self.authenticate()

        response = self.client.get('/api/auth/profile/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_courses'], 1)
        self.assertEqual(response.data['completed_lessons'], 1)
        self.assertEqual(response.data['total_lessons'], 2)
        self.assertEqual(response.data['progress_percentage'], 50)
        self.assertEqual(response.data['points_earned'], 10)

    def test_profile_settings_can_be_updated(self):
        self.authenticate()

        response = self.client.patch(
            '/api/auth/profile/',
            {
                'first_name': 'Maimuna',
                'username': 'maimuna-learner',
                'profile': {
                    'bio': 'Learning full-stack development.',
                    'theme': 'dark',
                    'email_notifications': False,
                },
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Maimuna')
        self.assertEqual(self.user.username, 'maimuna-learner')
        self.assertEqual(self.user.learner_profile.theme, 'dark')
        self.assertFalse(self.user.learner_profile.email_notifications)

    def test_profile_picture_can_be_uploaded_and_removed(self):
        self.authenticate()
        image = SimpleUploadedFile(
            'avatar.gif',
            (
                b'GIF89a\x01\x00\x01\x00\x80\x00\x00'
                b'\x00\x00\x00\xff\xff\xff!\xf9\x04\x01'
                b'\x00\x00\x00\x00,\x00\x00\x00\x00\x01'
                b'\x00\x01\x00\x00\x02\x02D\x01\x00;'
            ),
            content_type='image/gif',
        )

        upload_response = self.client.post(
            '/api/auth/profile/avatar/',
            {'avatar': image},
            format='multipart',
        )

        self.assertEqual(upload_response.status_code, status.HTTP_200_OK)
        self.assertIn('/media/profile-pictures/', upload_response.data['avatar_url'])
        self.user.refresh_from_db()
        uploaded_avatar = self.user.learner_profile.avatar
        self.assertTrue(uploaded_avatar)

        delete_response = self.client.delete('/api/auth/profile/avatar/')

        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.user.learner_profile.refresh_from_db()
        self.assertFalse(self.user.learner_profile.avatar)

    def test_authenticated_user_can_change_password(self):
        self.authenticate()

        response = self.client.post(
            '/api/auth/password/',
            {
                'current_password': 'strong-password-123',
                'new_password': 'new-strong-password-456',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new-strong-password-456'))

    def test_login_response_includes_staff_status(self):
        response = self.client.post(
            '/api/auth/login/',
            {
                'username': 'platform-admin@example.com',
                'password': 'admin-password-123',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['user']['is_staff'])
        self.assertTrue(response.data['user']['is_superuser'])

    def test_regular_user_cannot_access_admin_api(self):
        self.authenticate()

        response = self.client.get('/api/admin/users/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_user_course_and_lesson(self):
        self.authenticate(self.admin_user)

        user_response = self.client.post(
            '/api/admin/users/',
            {
                'username': 'new-student',
                'email': 'new-student@example.com',
                'password': 'strong-new-password-123',
                'is_active': True,
                'is_staff': False,
            },
            format='json',
        )
        course_response = self.client.post(
            '/api/admin/courses/',
            {
                'title': 'Admin Created Course',
                'slug': 'admin-created-course',
                'category': 'programming',
                'description': 'Created from the administrator dashboard.',
            },
            format='json',
        )
        lesson_response = self.client.post(
            '/api/admin/lessons/',
            {
                'course': course_response.data['id'],
                'title': 'First Lesson',
                'slug': 'admin-created-first-lesson',
                'content': 'Welcome to the lesson.',
                'order': 1,
            },
            format='json',
        )

        self.assertEqual(user_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(course_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(lesson_response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_block_user_but_not_themselves(self):
        self.authenticate(self.admin_user)

        blocked_response = self.client.patch(
            f'/api/admin/users/{self.user.id}/',
            {'is_active': False},
            format='json',
        )
        self_block_response = self.client.patch(
            f'/api/admin/users/{self.admin_user.id}/',
            {'is_active': False},
            format='json',
        )

        self.assertEqual(blocked_response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(self_block_response.status_code, status.HTTP_400_BAD_REQUEST)
