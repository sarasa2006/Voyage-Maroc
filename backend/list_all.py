
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from voyages.models import Lieu

all_lieux = Lieu.objects.all().order_by('ville', 'nom')
for l in all_lieux:
    print(f"{l.ville} | {l.nom}")
