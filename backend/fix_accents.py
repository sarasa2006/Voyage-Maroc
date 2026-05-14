
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from voyages.models import Lieu

def fix_accents():
    replacements = {
        '??': 'é',
        '': 'é',
        'M??dina': 'Médina',
        'Mdina': 'Médina',
        'F??s': 'Fès',
        'Fs': 'Fès',
        'Mosqu??e': 'Mosquée',
        'Mosque': 'Mosquée',
        'M??dersa': 'Médersa',
        'Mdersa': 'Médersa',
        'M??nara': 'Ménara',
        'Mus??e': 'Musée',
        'Muse': 'Musée',
        'Mausol??e': 'Mausolée',
        'Mausole': 'Mausolée',
        'Isma??l': 'Ismaïl',
        '??le': 'Île',
        'T??touan': 'Tétouan',
        'Mekn??s': 'Meknès',
    }

    lieux = Lieu.objects.all()
    fixed_count = 0

    for lieu in lieux:
        original_nom = lieu.nom
        original_desc = lieu.description
        original_ville = lieu.ville
        
        new_nom = original_nom
        new_desc = original_desc
        new_ville = original_ville
        
        for old, new in replacements.items():
            new_nom = new_nom.replace(old, new)
            new_desc = new_desc.replace(old, new)
            new_ville = new_ville.replace(old, new)
            
        if new_nom != original_nom or new_desc != original_desc or new_ville != original_ville:
            lieu.nom = new_nom
            lieu.description = new_desc
            lieu.ville = new_ville
            lieu.save()
            fixed_count += 1
            print(f"Fixe : {original_nom} -> {new_nom}")

    print(f"\nTermine ! {fixed_count} lieux corriges.")

if __name__ == "__main__":
    fix_accents()
