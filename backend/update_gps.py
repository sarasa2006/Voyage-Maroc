import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from voyages.models import Lieu

# Coordonnées GPS exactes par nom de lieu exact
GPS_EXACT = {
    'Place Jemaa el-Fna':              (31.6258,  -7.9892, 'Marrakech'),
    'Jardin Majorelle':                (31.6416,  -8.0032, 'Marrakech'),
    'Palais Bahia':                    (31.6214,  -7.9828, 'Marrakech'),
    'Souks de Marrakech':              (31.6328,  -7.9852, 'Marrakech'),
    'Tombeaux Saadiens':               (31.6183,  -7.9894, 'Marrakech'),
    'Koutoubia Mosque':                (31.6245,  -7.9937, 'Marrakech'),
    'Hammam El Bacha':                 (31.6347,  -7.9892, 'Marrakech'),
    'Médina de Fès el-Bali':          (34.0638,  -4.9733, 'Fès'),
    'Tanneries Chouara':               (34.0657,  -4.9704, 'Fès'),
    'Médersa Bou Inania':             (34.0641,  -4.9775, 'Fès'),
    'Mosquée al-Qarawiyyin':           (34.0645,  -4.9736, 'Fès'),
    'Borj Nord Museum':                (34.0712,  -4.9706, 'Fès'),
    'Médina Bleue de Chefchaouen':    (35.1681,  -5.2645, 'Chefchaouen'),
    'Place Uta el-Hammam':             (35.1683,  -5.2636, 'Chefchaouen'),
    'Cascades Ras el-Maa':             (35.1667,  -5.2557, 'Chefchaouen'),
    'Kasbah de Chefchaouen':           (35.1684,  -5.2635, 'Chefchaouen'),
    "Plage d'Agadir":                  (30.4202,  -9.5981, 'Agadir'),
    "Kasbah d'Agadir Oufella":        (30.4450,  -9.6092, 'Agadir'),
    "Souk El Had d'Agadir":           (30.4089,  -9.5714, 'Agadir'),
    'Parc Olhão Agadir':              (30.4167,  -9.5833, 'Agadir'),
    'Mosquée Hassan II':               (33.6086,  -7.6327, 'Casablanca'),
    'Corniche de Casablanca':          (33.5942,  -7.6681, 'Casablanca'),
    'Quartier Art Déco':              (33.5945,  -7.6188, 'Casablanca'),
    'Marché Central de Casablanca':   (33.5889,  -7.6092, 'Casablanca'),
    "Médina d'Essaouira":             (31.5085,  -9.7595, 'Essaouira'),
    "Remparts et Skala d'Essaouira":  (31.5118,  -9.7664, 'Essaouira'),
    "Plage d'Essaouira":              (31.5041,  -9.7444, 'Essaouira'),
    'Kasbah Aït Benhaddou':           (31.0472,  -7.1296, 'Ouarzazate'),
    'Studios Atlas Ouarzazate':        (30.9311,  -6.8937, 'Ouarzazate'),
    'Erg Chebbi - Dunes de Merzouga': (31.0800,  -3.9780, 'Merzouga'),
    'Bivouac Saharien Merzouga':       (31.0750,  -3.9680, 'Merzouga'),
    'Tour Hassan et Mausolée Mohammed V': (34.0248, -6.8206, 'Rabat'),
    'Kasbah des Oudayas Rabat':        (34.0325,  -6.8345, 'Rabat'),
    'Chellah Rabat':                   (34.0092,  -6.8308, 'Rabat'),
}

for nom, (lat, lng, ville) in GPS_EXACT.items():
    updated = Lieu.objects.filter(nom=nom).update(lat=lat, lng=lng, ville=ville)
    if updated:
        print(f"OK: {nom}")
    else:
        print(f"NOT FOUND: {nom}")

print("Done. Total lieux:", Lieu.objects.count())
print("Avec GPS:", Lieu.objects.filter(lat__isnull=False).count())
