from .models import Favori

def favori_count(request):
    """Fournit le nombre d'éléments dans le plan (panier) pour tous les templates."""
    if request.user.is_authenticated:
        count = Favori.objects.filter(utilisateur=request.user).count()
        return {'favori_count': count}
    return {'favori_count': 0}
