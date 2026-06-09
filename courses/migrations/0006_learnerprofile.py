from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0005_seed_course_catalog'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=280)),
                ('avatar_url', models.URLField(blank=True, max_length=500)),
                ('role', models.CharField(choices=[('student', 'Student'), ('premium', 'Premium Member'), ('instructor', 'Instructor')], default='student', max_length=20)),
                ('email_notifications', models.BooleanField(default=True)),
                ('push_notifications', models.BooleanField(default=True)),
                ('course_announcements', models.BooleanField(default=True)),
                ('deadline_reminders', models.BooleanField(default=True)),
                ('forum_replies', models.BooleanField(default=False)),
                ('theme', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('system', 'System')], default='light', max_length=10)),
                ('autoplay_next_lesson', models.BooleanField(default=True)),
                ('caption_language', models.CharField(default='English', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='learner_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
