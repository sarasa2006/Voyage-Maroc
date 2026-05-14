
"""
Script pour pré-remplir la BDD avec de vrais lieux marocains (coordonnées GPS réelles).
Lancez avec : python manage.py shell < seed_lieux.py
"""
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from voyages.models import Lieu

# Supprimer les anciens lieux pour repartir sur une base propre
Lieu.objects.all().delete()

LIEUX_MAROC = [
    # ====== MARRAKECH ======
    {"nom": "Place Jemaa el-Fna", "categorie": "Culture", "cout": 50, "ville": "Marrakech", "lat": 31.6258, "lng": -7.9892,
     "description": "La place mythique de Marrakech.Budget estimé pour jus d'orange, henné et petits spectacles.",
       "image": "lieux/jemaa_el_fna.png"},
    {"nom": "Jardin Majorelle", "categorie": "Nature", "cout": 180, "ville": "Marrakech", "lat": 31.6416, "lng": -8.0032,
     "description": "Jardin botanique exceptionnel. Le tarif inclut l'accès au jardin et au musée Pierre Bergé.",
      "image": "lieux/jardin_majorelle.png"},
    {"nom": "Palais Bahia", "categorie": "Histoire", "cout": 80, "ville": "Marrakech", "lat": 31.6214, "lng": -7.9828, "description": "Magnifique palais du XIXe siècle. Chef-d'œuvre de l'architecture marocaine."},
    {"nom": "Souks de Marrakech", "categorie": "Gastronomie", "cout": 100, "ville": "Marrakech", "lat": 31.6328, "lng": -7.9852, "description": "Labyrinthe commerçant. Budget pour une dégustation de pâtisseries et thé."},
    {"nom": "Tombeaux Saadiens", "categorie": "Histoire", "cout": 80, "ville": "Marrakech", "lat": 31.6183, "lng": -7.9894, "description": "Nécropole royale datant du XVIe siècle."},
    {"nom": "Koutoubia Mosque", "categorie": "Culture", "cout": 0, "ville": "Marrakech", "lat": 31.6245, "lng": -7.9937, "description": "Symbole de Marrakech (accès extérieur gratuit)."},
    {"nom": "Hammam El Bacha", "categorie": "Détente", "cout": 250, "ville": "Marrakech", "lat": 31.6347, "lng": -7.9892, "description": "Hammam historique de luxe pour une relaxation totale."},

    # ====== FÈS ======
    {"nom": "Médina de Fès el-Bali", "categorie": "Histoire", "cout": 0, "ville": "Fès", "lat": 34.0638, "lng": -4.9733, "description": "Plus grande médina médiévale du monde, classée au patrimoine mondial de l'UNESCO. Un vrai voyage dans le temps."},
    {"nom": "Tanneries Chouara", "categorie": "Culture", "cout": 20, "ville": "Fès", "lat": 34.0657, "lng": -4.9704, "description": "Les célèbres tanneries de Fès sont un spectacle unique. Depuis les terrasses des tanneurs, vue imprenable sur les cuves colorées."},
    {"nom": "Médersa Bou Inania", "categorie": "Histoire", "cout": 30, "ville": "Fès", "lat": 34.0641, "lng": -4.9775, "description": "Bijou de l'architecture mérinide du XIVe siècle. Ses zelliges, ses sculptures en bois de cèdre et son marbre sont saisissants."},
    {"nom": "Mosquée al-Qarawiyyin", "categorie": "Culture", "cout": 0, "ville": "Fès", "lat": 34.0645, "lng": -4.9736, "description": "Fondée en 859, c'est l'une des plus anciennes universités du monde encore en activité."},
    {"nom": "Borj Nord Museum", "categorie": "Histoire", "cout": 20, "ville": "Fès", "lat": 34.0712, "lng": -4.9706, "description": "Ancienne forteresse reconvertie en musée des armes, offrant une vue panoramique sur Fès."},

    # ====== CHEFCHAOUEN ======
    {"nom": "Médina Bleue de Chefchaouen", "categorie": "Culture", "cout": 0, "ville": "Chefchaouen", "lat": 35.1681, "lng": -5.2645, "description": "La ville bleue du Rif, dont les ruelles peintes en bleu et blanc offrent un décor de conte de fées unique au monde.", "image": "lieux/chefchaouen.png"},
    {"nom": "Place Uta el-Hammam", "categorie": "Gastronomie", "cout": 0, "ville": "Chefchaouen", "lat": 35.1683, "lng": -5.2636, "description": "Place centrale animée de Chefchaouen, entourée de cafés et restaurants. Idéale pour déguster un thé à la menthe."},
    {"nom": "Cascades Ras el-Maa", "categorie": "Nature", "cout": 0, "ville": "Chefchaouen", "lat": 35.1667, "lng": -5.2557, "description": "Source d'eau naturelle à l'entrée de la médina, point de départ de randonnées dans les montagnes du Rif."},
    {"nom": "Kasbah de Chefchaouen", "categorie": "Histoire", "cout": 10, "ville": "Chefchaouen", "lat": 35.1684, "lng": -5.2635, "description": "Ancienne forteresse du XVe siècle au cœur de la médina avec un joli jardin andalou et un musée ethnographique."},

    # ====== AGADIR ======
    {"nom": "Plage d'Agadir", "categorie": "Plage", "cout": 0, "ville": "Agadir", "lat": 30.4202, "lng": -9.5981, "description": "Plage de sable fin de 10km de long, ensoleillée 300 jours par an. Idéale pour le surf, la baignade et les sports nautiques."},
    {"nom": "Kasbah d'Agadir Oufella", "categorie": "Histoire", "cout": 30, "ville": "Agadir", "lat": 30.4450, "lng": -9.6092, "description": "Vestiges de l'ancienne citadelle sur la colline dominant Agadir, avec une vue panoramique sur la baie et la ville."},
    {"nom": "Souk El Had d'Agadir", "categorie": "Gastronomie", "cout": 0, "ville": "Agadir", "lat": 30.4089, "lng": -9.5714, "description": "Le grand marché d'Agadir, l'un des plus grands du Maroc avec plus de 6000 commerçants sur 15 hectares."},
    {"nom": "Parc Olhão Agadir", "categorie": "Nature", "cout": 0, "ville": "Agadir", "lat": 30.4167, "lng": -9.5833, "description": "Parc verdoyant en bord de mer, parfait pour se reposer, se balade et observer la faune locale."},

    # ====== CASABLANCA ======
    {"nom": "Mosquée Hassan II", "categorie": "Culture", "cout": 150, "ville": "Casablanca", "lat": 33.6086, "lng": -7.6327, "description": "Visite guidée de l'une des plus grandes mosquées au monde.", "image": "lieux/hassan_ii.png"},
    {"nom": "Corniche de Casablanca", "categorie": "Détente", "cout": 50, "ville": "Casablanca", "lat": 33.5942, "lng": -7.6681, "description": "Balade en bord de mer (budget café/glace)."},
    {"nom": "Quartier Art Déco", "categorie": "Histoire", "cout": 0, "ville": "Casablanca", "lat": 33.5945, "lng": -7.6188, "description": "Centre-ville historique avec une collection exceptionnelle de bâtiments Art Déco des années 1930-40."},
    {"nom": "Marché Central de Casablanca", "categorie": "Gastronomie", "cout": 0, "ville": "Casablanca", "lat": 33.5889, "lng": -7.6092, "description": "Marché couvert proposant poissons frais, épices, légumes et produits artisanaux en plein cœur de la ville."},

    # ====== ESSAOUIRA ======
    {"nom": "Médina d'Essaouira", "categorie": "Histoire", "cout": 0, "ville": "Essaouira", "lat": 31.5085, "lng": -9.7595, "description": "Cité forteresse classée UNESCO. Ses remparts blancs et bleus face à l'Atlantique lui donnent un charme unique."},
    {"nom": "Remparts et Skala d'Essaouira", "categorie": "Histoire", "cout": 0, "ville": "Essaouira", "lat": 31.5118, "lng": -9.7664, "description": "Les remparts du XVIIIe siècle offrent une promenade spectaculaire face à l'océan Atlantique."},
    {"nom": "Plage d'Essaouira", "categorie": "Plage", "cout": 0, "ville": "Essaouira", "lat": 31.5041, "lng": -9.7444, "description": "Grande plage ventée, paradis des surfeurs et kite-surfeurs. Le vent constant (Alizé) en fait un spot de renommée mondiale."},

    # ====== OUARZAZATE ======
    {"nom": "Kasbah Aït Benhaddou", "categorie": "Histoire", "cout": 50, "ville": "Ouarzazate", "lat": 31.0472, "lng": -7.1296, "description": "Ksar fortifié classé UNESCO et décor naturel de films hollywoodiens (Gladiator, Game of Thrones). Architectural grandiose."},
    {"nom": "Studios Atlas Ouarzazate", "categorie": "Culture", "cout": 80, "ville": "Ouarzazate", "lat": 30.9311, "lng": -6.8937, "description": "Les plus grands studios de cinéma à ciel ouvert au monde. Hollywood d'Afrique avec ses décors géants."},

    # ====== MERZOUGA (SAHARA) ======
    {"nom": "Erg Chebbi - Dunes de Merzouga", "categorie": "Nature", "cout": 300, "ville": "Merzouga", "lat": 31.0800, "lng": -3.9780, "description": "Les spectaculaires dunes de sable orange pouvant atteindre 150m de hauteur. Balade en dromadaire et bivouac sous les étoiles."},
    {"nom": "Bivouac Saharien Merzouga", "categorie": "Aventure", "cout": 600, "ville": "Merzouga", "lat": 31.0750, "lng": -3.9680, "description": "Nuit en tente berbère au cœur du Sahara, dîner aux bougies, musique gnawa et lever de soleil sur les dunes."},

    # ====== RABAT ======
    {"nom": "Tour Hassan et Mausolée Mohammed V", "categorie": "Histoire", "cout": 0, "ville": "Rabat", "lat": 34.0248, "lng": -6.8206, "description": "Minaret inachevé du XIIe siècle face au mausolée royal. L'un des sites les plus majestueux du Maroc."},
    {"nom": "Kasbah des Oudayas Rabat", "categorie": "Histoire", "cout": 0, "ville": "Rabat", "lat": 34.0325, "lng": -6.8345, "description": "Citadelle almohade à l'embouchure du Bouregreg. Ses ruelles colorées et son jardin andalou sont magnifiques."},
    {"nom": "Chellah Rabat", "categorie": "Histoire", "cout": 20, "ville": "Rabat", "lat": 34.0092, "lng": -6.8308, "description": "Nécropole médiévale et site romain en plein cœur de Rabat, habitée par des cigognes et des nénuphars."},

    # ====== TANGER ======
    {"nom": "Grotte d'Hercule", "categorie": "Nature", "cout": 10, "ville": "Tanger", "lat": 35.7602, "lng": -5.9398, "description": "Grottes naturelles à l'ouverture en forme de carte d'Afrique inversée."},
    {"nom": "Cap Spartel", "categorie": "Nature", "cout": 0, "ville": "Tanger", "lat": 35.7901, "lng": -5.9231, "description": "Point de rencontre entre l'Atlantique et la Méditerranée."},
    {"nom": "Kasbah de Tanger", "categorie": "Histoire", "cout": 20, "ville": "Tanger", "lat": 35.7891, "lng": -5.8123, "description": "Ancien palais du sultan et musée de la Kasbah offrant une vue sur le détroit."},

    # ====== MEKNÈS ======
    {"nom": "Bab Mansour", "categorie": "Histoire", "cout": 0, "ville": "Meknès", "lat": 33.8976, "lng": -5.5633, "description": "La plus belle porte du Maroc et d'Afrique du Nord."},
    {"nom": "Volubilis", "categorie": "Histoire", "cout": 70, "ville": "Meknès", "lat": 34.0733, "lng": -5.5544, "description": "Cité antique romaine la mieux préservée du Maroc, classée UNESCO."},
    {"nom": "Mausolée de Moulay Ismaïl", "categorie": "Culture", "cout": 0, "ville": "Meknès", "lat": 33.8936, "lng": -5.5651, "description": "Dernière demeure du grand sultan bâtisseur de Meknès."},

    # ====== IFRANE ======
    {"nom": "Lion d'Ifrane", "categorie": "Culture", "cout": 0, "ville": "Ifrane", "lat": 33.5271, "lng": -5.1054, "description": "Sculpture emblématique taillée dans la roche pendant la Seconde Guerre mondiale."},
    {"nom": "Parc National d'Ifrane", "categorie": "Nature", "cout": 0, "ville": "Ifrane", "lat": 33.4500, "lng": -5.1500, "description": "Forêts de cèdres millénaires et singes magots en liberté."},

    # ====== DAKHLA ======
    {"nom": "Dune Blanche", "categorie": "Nature", "cout": 0, "ville": "Dakhla", "lat": 23.7128, "lng": -15.9452, "description": "Dune de sable blanc éclatant plongeant dans le lagon turquoise."},
    {"nom": "Île du Dragon", "categorie": "Aventure", "cout": 150, "ville": "Dakhla", "lat": 23.8211, "lng": -15.8234, "description": "Excursion en bateau vers cette île déserte pour la randonnée et la détente."},

    # ====== TÉTOUAN ======
    {"nom": "Médina de Tétouan", "categorie": "Histoire", "cout": 0, "ville": "Tétouan", "lat": 35.5711, "lng": -5.3697, "description": "Une des plus petites médinas du Maroc mais la plus complète, classée UNESCO."},
    {"nom": "Musée Archéologique", "categorie": "Culture", "cout": 10, "ville": "Tétouan", "lat": 35.5722, "lng": -5.3711, "description": "Importante collection d'objets provenant du nord du Maroc, de la préhistoire à l'ère islamique."},
]

created_count = 0
for data in LIEUX_MAROC:
    # On utilise update_or_create pour mettre à jour les prix si ils ont changé
    obj, created = Lieu.objects.update_or_create(
        nom=data['nom'],
        defaults={
            'ville': data['ville'],
            'categorie': data['categorie'],
            'cout': data['cout'],
            'description': data['description'],
            'lat': data.get('lat'),
            'lng': data.get('lng'),
            'image': data.get('image'),
        }
    )
    if created:
        created_count += 1
        print(f"Cree : {data['nom']} ({data['ville']})")
    else:
        print(f"Mis a jour : {data['nom']}")

print(f"\nTermine ! {created_count} nouveaux lieux ajoutes sur {len(LIEUX_MAROC)} total.")
