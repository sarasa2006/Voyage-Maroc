import os
import urllib.request
import time

places = [
    "Place Jemaa el-Fna", "Jardin Majorelle", "Palais Bahia", "Souks de Marrakech", "Tombeaux Saadiens", "Koutoubia Mosque", "Hammam El Bacha",
    "Médina de Fès el-Bali", "Tanneries Chouara", "Médersa Bou Inania", "Mosquée al-Qarawiyyin", "Borj Nord Museum",
    "Médina Bleue de Chefchaouen", "Place Uta el-Hammam", "Cascades Ras el-Maa", "Kasbah de Chefchaouen",
    "Plage d'Agadir", "Kasbah d'Agadir Oufella", "Souk El Had d'Agadir", "Parc Olhão Agadir",
    "Mosquée Hassan II", "Corniche de Casablanca", "Quartier Art Déco", "Marché Central de Casablanca",
    "Médina d'Essaouira", "Remparts et Skala d'Essaouira", "Plage d'Essaouira",
    "Kasbah Aït Benhaddou", "Studios Atlas Ouarzazate",
    "Erg Chebbi - Dunes de Merzouga", "Bivouac Saharien Merzouga",
    "Tour Hassan et Mausolée Mohammed V", "Kasbah des Oudayas Rabat", "Chellah Rabat",
    "Grotte d'Hercule", "Cap Spartel", "Kasbah de Tanger",
    "Bab Mansour", "Volubilis", "Mausolée de Moulay Ismaïl",
    "Lion d'Ifrane", "Parc National d'Ifrane",
    "Dune Blanche", "Île du Dragon",
    "Médina de Tétouan", "Musée Archéologique"
]

os.makedirs('media/lieux', exist_ok=True)

for place in places:
    filename = "".join([c if c.isalnum() else "_" for c in place]).lower() + ".jpg"
    filepath = os.path.join('media/lieux', filename)
    if os.path.exists(filepath):
        continue
        
    url = f"https://picsum.photos/seed/{place.replace(' ', '_')}/800/600"
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Success: {filename}")
        time.sleep(0.5) # Prevent rate limiting
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
