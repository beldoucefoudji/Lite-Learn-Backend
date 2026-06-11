import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import LearnerProfile  # Import your profile model

User = get_user_model()

username = "admin"
email = "admin@example.com"
password = "YourSecurePassword123!"  # Swap this with your actual password!

if not User.objects.filter(username=username).exists():
    # 1. Create the admin user
    admin_user = User.objects.create_superuser(username=username, email=email, password=password)
    
    # 2. Safely link their missing profile row
    LearnerProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'role': 'instructor',
            'bio': 'System Administrator',
        }
    )
    print("🎉 Production superuser and LearnerProfile created successfully!")
else:
    
    admin_user = User.objects.get(username=username)
    LearnerProfile.objects.get_or_create(user=admin_user, defaults={'role': 'instructor'})
    print("Superuser profile verified.")