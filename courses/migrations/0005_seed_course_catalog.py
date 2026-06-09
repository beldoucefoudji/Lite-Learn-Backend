from django.db import migrations


COURSES = [
    {
        'title': 'Mastering TypeScript',
        'slug': 'mastering-typescript',
        'category': 'programming',
        'description': 'Deep dive into static typing, generics, and decorative patterns to build scalable applications.',
    },
    {
        'title': 'UX Design Fundamentals',
        'slug': 'ux-design-fundamentals',
        'category': 'web_dev',
        'description': 'Learn the psychological principles behind great user experiences and master modern interface design.',
    },
    {
        'title': 'Data Systems at Scale',
        'slug': 'data-systems-at-scale',
        'category': 'programming',
        'description': 'Understand distributed systems, database sharding, and high-availability architecture.',
    },
    {
        'title': 'Product Strategy 101',
        'slug': 'product-strategy-101',
        'category': 'web_dev',
        'description': 'Define a vision, create roadmaps, and manage stakeholders in a high-growth technical organization.',
    },
    {
        'title': 'Rust for WebAssembly',
        'slug': 'rust-for-webassembly',
        'category': 'programming',
        'description': 'Leverage the power of Rust on the web to build blazing-fast applications with near-native performance.',
    },
    {
        'title': 'Growth Marketing 101',
        'slug': 'growth-marketing-101',
        'category': 'web_dev',
        'description': 'Master user acquisition, funnel optimization, experimentation, and data-driven decision making.',
    },
]


def seed_catalog(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Lesson = apps.get_model('courses', 'Lesson')

    for course_data in COURSES:
        course, _ = Course.objects.get_or_create(
            slug=course_data['slug'],
            defaults=course_data,
        )
        Lesson.objects.get_or_create(
            course=course,
            order=1,
            defaults={
                'title': 'Introduction',
                'slug': f"{course.slug}-introduction",
                'content': f"Welcome to {course.title}. Learn the core concepts and prepare your development environment.",
            },
        )
        Lesson.objects.get_or_create(
            course=course,
            order=2,
            defaults={
                'title': 'Core Concepts',
                'slug': f"{course.slug}-core-concepts",
                'content': f"Explore the essential tools, techniques, and practical workflows used in {course.title}.",
            },
        )


def remove_seeded_catalog(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Course.objects.filter(slug__in=[course['slug'] for course in COURSES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0004_alter_lesson_options_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_catalog, remove_seeded_catalog),
    ]
