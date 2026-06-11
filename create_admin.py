import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Clean strings with no hidden characters
username = "admin"
email = "admin@example.com"
password = "YourSecurePassword123!"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("🎉 Production superuser created successfully!")
else:
    print("Superuser already exists.")