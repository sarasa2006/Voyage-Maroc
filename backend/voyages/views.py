from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Lieu, Voyage
from .forms import VoyageForm


class LieuListView(ListView):
    model = Lieu
    template_name = 'voyages/lieu_list.html'
    context_object_name = 'lieux'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(nom__icontains=query) | queryset.filter(ville__icontains=query)
        return queryset

class LieuDetailView(DetailView):
    model = Lieu
    template_name = 'voyages/lieu_detail.html'
    context_object_name = 'lieu'


class VoyageCreateView(LoginRequiredMixin, CreateView):
    """Crée un voyage à partir du formulaire (équivalent de la commande dans e-commerce)."""
    model = Voyage
    form_class = VoyageForm
    template_name = 'voyages/voyage_form.html'

    def form_valid(self, form):
        from favoris.models import Favori
        from .models import Itineraire
        from django.contrib import messages
        from django.shortcuts import redirect
        
        # Récupère tous les favoris actuels
        favoris = Favori.objects.filter(utilisateur=self.request.user)
        
        if not favoris.exists():
            messages.error(self.request, "⚠️ Votre plan est vide. Ajoutez des lieux avant de créer un voyage !")
            return redirect('favori_list')

        # Associe automatiquement le voyage à l'utilisateur connecté
        form.instance.utilisateur = self.request.user
        response = super().form_valid(form)
        
        # Crée un itinéraire par défaut (Jour 1) avec tous les lieux du plan
        itineraire = Itineraire.objects.create(voyage=self.object, jour=1)
        for f in favoris:
            itineraire.lieux.add(f.lieu)
        
        # Vider le plan (équivalent de vider le panier après commande)
        favoris.delete()
        
        messages.success(self.request, f"🚀 Voyage pour {self.object.destination} créé avec succès !")
        return response

    def get_success_url(self):
        return reverse_lazy('voyage_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Passe les favoris de l'utilisateur pour les afficher dans le formulaire
        from favoris.models import Favori
        ctx['favoris'] = Favori.objects.filter(
            utilisateur=self.request.user
        ).select_related('lieu')
        ctx['total'] = sum(f.lieu.cout for f in ctx['favoris'])
        return ctx


class VoyageDetailView(LoginRequiredMixin, DetailView):
    """Affiche les détails d'un voyage confirmé (équivalent de la confirmation de commande)."""
    model = Voyage
    template_name = 'voyages/voyage_confirm.html'
    context_object_name = 'voyage'

    def get_queryset(self):
        # Un utilisateur ne peut voir que ses propres voyages
        return Voyage.objects.filter(utilisateur=self.request.user)


class VoyageListView(LoginRequiredMixin, ListView):
    """Affiche l'historique des voyages confirmés de l'utilisateur."""
    model = Voyage
    template_name = 'voyages/voyage_list.html'
    context_object_name = 'voyages'

    def get_queryset(self):
        return Voyage.objects.filter(utilisateur=self.request.user).order_by('-date_creation')