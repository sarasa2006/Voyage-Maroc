
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from voyages.models import Lieu
from django.db.models import Q

# On cherche les lieux où l'image est vide ou nulle
missing = Lieu.objects.filter(Q(image='') | Q(image__isnull=True)).order_by('ville', 'nom')

print("VILLE | NOM")
for l in missing:
    print(f"{l.ville} | {l.nom}")
