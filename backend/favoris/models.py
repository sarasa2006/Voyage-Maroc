
from django.db import models
from users.models import CustomUser
from voyages.models import Lieu

class Favori(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.utilisateur} - {self.lieu}"