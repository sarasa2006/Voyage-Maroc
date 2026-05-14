import os
import django
import unicodedata
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from voyages.models import Lieu

def normalize_string(s):
    """Supprime les accents et les caractères spéciaux pour la comparaison."""
    s = unicodedata.normalize('NFD', s)
    s = s.encode('ascii', 'ignore').decode('utf-8')
    s = s.lower()
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

def assign_images():
    media_path = os.path.join('media', 'lieux')
    if not os.path.exists(media_path):
        print(f"Erreur: Le dossier {media_path} n'existe pas.")
        return

    # Scanner tous les fichiers du dossier media/lieux
    available_files = {}
    for f in os.listdir(media_path):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            norm_name = normalize_string(os.path.splitext(f)[0])
            available_files[norm_name] = f

    print(f"Fichiers trouves dans {media_path} : {len(available_files)}")

    lieux = Lieu.objects.all()
    assigned_count = 0

    for lieu in lieux:
        # On normalise le nom du lieu pour chercher une correspondance
        norm_lieu = normalize_string(lieu.nom)
        
        # 1. Tentative de correspondance exacte normalisée
        found_file = available_files.get(norm_lieu)
        
        # 2. Si pas trouvé, tentative avec le nom de la ville + nom lieu
        if not found_file:
            norm_lieu_ville = normalize_string(lieu.ville + lieu.nom)
            found_file = available_files.get(norm_lieu_ville)
            
        # 3. Si toujours pas trouvé, on cherche si une clé contient le nom du lieu
        if not found_file:
            for key, filename in available_files.items():
                if norm_lieu in key or key in norm_lieu:
                    found_file = filename
                    break

        if found_file:
            lieu.image = f"lieux/{found_file}"
            lieu.save()
            assigned_count += 1
            print(f"Assigne : {found_file} -> {lieu.nom}")
        else:
            print(f"Attention : Aucune image trouvee pour '{lieu.nom}' (cherché: {norm_lieu})")

    print(f"\nTermine ! {assigned_count} images liees aux lieux.")

if __name__ == "__main__":
    assign_images()
