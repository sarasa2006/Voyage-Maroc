import json
import random
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from voyages.models import Lieu

CATEGORIES_MAROC = {
    'culture':       ['Culture', 'Histoire', 'Patrimoine', 'Art', 'Musée'],
    'nature':        ['Nature', 'Parc', 'Montagne', 'Foret', 'Desert', 'Oasis'],
    'plage':         ['Plage', 'Balnéaire', 'Mer', 'Côte'],
    'gastronomie':   ['Gastronomie', 'Restaurant', 'Cuisine', 'Marché'],
    'aventure':      ['Aventure', 'Sport', 'Trek', 'Surf'],
    'detente':       ['Détente', 'Spa', 'Hammam', 'Bien-être'],
}

VILLES_DISPONIBLES = [
    'Marrakech', 'Fès', 'Chefchaouen', 'Agadir', 'Casablanca',
    'Essaouira', 'Ouarzazate', 'Merzouga', 'Rabat',
]

# Centre de chaque ville (pour la carte initiale)
VILLE_CENTRES = {
    'Marrakech':    (31.6295, -7.9811),
    'Fès':          (34.0531, -4.9998),
    'Chefchaouen':  (35.1681, -5.2636),
    'Agadir':       (30.4278, -9.5981),
    'Casablanca':   (33.5731, -7.5898),
    'Essaouira':    (31.5085, -9.7595),
    'Ouarzazate':   (30.9202, -6.8936),
    'Merzouga':     (31.0983, -3.9731),
    'Rabat':        (34.0209, -6.8416),
}

REPONSES_CHATBOT = {
    'bonjour': "Bonjour ! Je suis votre assistant voyage Maroc. Comment puis-je vous aider ?",
    'salut': "Salut ! Prêt à planifier votre voyage au Maroc ? 🇲🇦",
    'marrakech': "Marrakech, la 'Ville Rose', est incontournable ! Visitez la Place Jemaa el-Fna, les Souks, le Jardin Majorelle et les palais historiques. Durée recommandée : 3 jours.",
    'fes': "Fès est la capitale spirituelle du Maroc. La médina de Fès el-Bali est classée UNESCO. À ne pas manquer : la tannerie Chouara, la médersa Bou Inania et le quartier des bronziers.",
    'chefchaouen': "Chefchaouen, la 'Ville Bleue', est un bijou nichée dans le Rif. Prévoyez 2 jours pour vous perdre dans ses ruelles bleues et violettes. Idéale pour la photographie !",
    'sahara': "Le désert du Sahara marocain, notamment Merzouga et Erg Chebbi, offre une expérience inoubliable. Balade en dromadaire, nuit sous les étoiles en bivouac, lever de soleil sur les dunes.",
    'casablanca': "Casablanca est la métropole économique du Maroc. La Mosquée Hassan II est l'une des plus grandes du monde. Le quartier Art déco du centre-ville vaut le détour.",
    'agadir': "Agadir est la station balnéaire numéro 1 du Maroc. Plage de sable fin, soleil toute l'année, souk d'Agadir et Kasbah sont les principales attractions.",
    'budget': "Pour un voyage économique au Maroc, comptez entre 300 et 500 MAD/jour. Pour un voyage confort : 800-1500 MAD/jour. Les transports CTM entre villes sont très abordables.",
    'visa': "Les ressortissants de la plupart des pays n'ont pas besoin de visa pour le Maroc pour un séjour de moins de 90 jours.",
    'transport': "Pour voyager au Maroc : Train (ONCF) entre grandes villes, Bus CTM ou Supratours, taxis grands axes, ou voitures de location.",
    'nourriture': "La cuisine marocaine est délicieuse ! Ne manquez pas : le tajine, le couscous, la pastilla, les brochettes, le thé à la menthe et les pâtisseries orientales.",
    'meteo': "Le Maroc a un climat varié : la côte atlantique est douce toute l'année. Le sud (Sahara) est chaud en été. Les montagnes peuvent être enneigées en hiver.",
    'aide': "Je peux vous informer sur : les villes (Marrakech, Fès, Chefchaouen...), le budget, le visa, les transports, la nourriture. Que voulez-vous savoir ?",
    'merci': "Avec plaisir ! N'hésitez pas si vous avez d'autres questions. 🌟",
}

def get_reponse_chatbot(message):
    msg = message.lower().strip()
    for mot_cle, reponse in REPONSES_CHATBOT.items():
        if mot_cle in msg:
            return reponse
    if any(mot in msg for mot in ['comment', 'où', 'quand', 'pourquoi', 'combien']):
        return "Je ne suis pas sûr de comprendre. Tapez 'aide' pour voir ce que je peux faire !"
    return "Je suis spécialisé dans les voyages au Maroc 🇲🇦. Posez-moi des questions sur les destinations, le budget, les transports ou la nourriture !"


def recommander_lieux(ville, budget_total, nb_jours, categorie_pref):
    """
    Filtre les lieux de la ville choisie selon catégorie + budget.
    Retourne un itinéraire jour par jour + les données GPS pour la carte Leaflet.
    """
    budget_par_jour = budget_total / max(nb_jours, 1)
    mots_cles = CATEGORIES_MAROC.get(categorie_pref.lower(), [categorie_pref])

    # Filtrer par ville (insensible à la casse)
    lieux_ville = Lieu.objects.filter(ville__iexact=ville)

    # Appliquer le filtre catégorie
    lieux_cat = [l for l in lieux_ville if any(mc.lower() in l.categorie.lower() for mc in mots_cles)]

    # Appliquer le filtre budget
    lieux_budget = [l for l in lieux_cat if l.cout is None or l.cout <= budget_par_jour]

    # Fallback progressif
    if not lieux_budget:
        lieux_budget = list(lieux_cat) or list(lieux_ville) or list(Lieu.objects.all())

    # Construire l'itinéraire jour par jour (on s'assure d'avoir nb_jours)
    itineraire = []
    
    # On prépare un pool cyclique pour être sûr de remplir tous les jours demandés
    # même s'il n'y a pas assez de lieux uniques
    pool = list(lieux_budget)
    if not pool:
        pool = list(Lieu.objects.all()[:10]) # Hard fallback
        
    for jour in range(1, nb_jours + 1):
        # On prend 2 lieux par jour. Si on arrive au bout du pool, on recommence au début.
        idx1 = ((jour - 1) * 2) % len(pool)
        idx2 = ((jour - 1) * 2 + 1) % len(pool)
        
        lieux_du_jour = [pool[idx1]]
        # On ajoute un 2ème lieu différent du premier si possible
        if pool[idx1] != pool[idx2]:
            lieux_du_jour.append(pool[idx2])
            
        itineraire.append({'jour': jour, 'lieux': lieux_du_jour})

    # Données GPS pour Leaflet (uniquement les lieux avec coords)
    markers = []
    seen = set()
    for l in lieux_budget:
        if l.lat and l.lng and l.id not in seen:
            markers.append({
                'id': l.id,
                'nom': l.nom,
                'lat': l.lat,
                'lng': l.lng,
                'categorie': l.categorie,
                'cout': l.cout,
                'description': l.description[:100] if l.description else '',
                'image_url': l.image.url if l.image else None,
            })
            seen.add(l.id)

    return itineraire, markers


# =====================================================================
#  VUE RECOMMANDATIONS IA
# =====================================================================
class RecommandationView(View):
    def get(self, request):
        return render(request, 'assistant_ia/recommandation.html', {
            'categories': list(CATEGORIES_MAROC.keys()),
            'villes': VILLES_DISPONIBLES,
            'itineraire': None,
            'markers_json': '[]',
            'centre_json': json.dumps({'lat': 31.7917, 'lng': -7.0926, 'zoom': 6}),
        })

    def post(self, request):
        try:
            budget    = float(request.POST.get('budget', 1500))
            nb_jours  = int(request.POST.get('nb_jours', 3))
            categorie = request.POST.get('categorie', 'culture')
            ville     = request.POST.get('ville', 'Marrakech')
        except (ValueError, TypeError):
            budget, nb_jours, categorie, ville = 1500, 3, 'culture', 'Marrakech'

        itineraire, markers = recommander_lieux(ville, budget, nb_jours, categorie)

        # Centre de la carte = ville choisie
        lat_c, lng_c = VILLE_CENTRES.get(ville, (31.7917, -7.0926))
        centre = {'lat': lat_c, 'lng': lng_c, 'zoom': 14 if markers else 6}

        context = {
            'categories': list(CATEGORIES_MAROC.keys()),
            'villes': VILLES_DISPONIBLES,
            'itineraire': itineraire,
            'budget': budget,
            'nb_jours': nb_jours,
            'categorie': categorie,
            'ville': ville,
            'nb_lieux': len(markers),
            'markers_json': json.dumps(markers, ensure_ascii=False),
            'centre_json': json.dumps(centre),
        }
        return render(request, 'assistant_ia/recommandation.html', context)


# =====================================================================
#  VUE CHATBOT
# =====================================================================
class ChatbotView(View):
    def get(self, request):
        return render(request, 'assistant_ia/chatbot.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
        except (json.JSONDecodeError, AttributeError):
            message = request.POST.get('message', '')
        reponse = get_reponse_chatbot(message)
        return JsonResponse({'response': reponse, 'status': 'ok'})



