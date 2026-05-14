
from django.db import models
from users.models import CustomUser

class Voyage(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    duree = models.IntegerField()
    budget = models.FloatField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.destination


VILLES_MAROC = [
    'Marrakech', 'Fès', 'Chefchaouen', 'Agadir', 'Casablanca',
    'Essaouira', 'Ouarzazate', 'Merzouga', 'Rabat', 'Tanger',
    'Meknès', 'Ifrane', 'Dakhla', 'Tétouan',
]

class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    ville = models.CharField(max_length=100, default='Marrakech')
    categorie = models.CharField(max_length=50)
    cout = models.FloatField(default=0)
    description = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='lieux/', null=True, blank=True)
    # Coordonnées GPS pour Google Maps
    lat = models.FloatField(null=True, blank=True, help_text="Latitude GPS")
    lng = models.FloatField(null=True, blank=True, help_text="Longitude GPS")

    def __str__(self):
        return f"{self.nom} ({self.ville})"


class Itineraire(models.Model):
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE)
    jour = models.IntegerField()
    lieux = models.ManyToManyField(Lieu)

    def __str__(self):
        return f"{self.voyage} - Jour {self.jour}"