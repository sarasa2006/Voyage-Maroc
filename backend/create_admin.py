import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Check if admin user exists
u = User.objects.filter(username='admin').first()
if u:
    u.set_password('admin123')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('Password reset and permissions granted for existing admin user.')
else:
    User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print('Superuser created successfully.')
