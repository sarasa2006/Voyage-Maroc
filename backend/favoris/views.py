from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Favori
from voyages.models import Lieu


class FavoriListView(LoginRequiredMixin, ListView):
    """Affiche la liste des lieux favoris de l'utilisateur connecté (équivalent 'panier')."""
    model = Favori
    template_name = 'favoris/favori_list.html'
    context_object_name = 'favoris'

    def get_queryset(self):
        return Favori.objects.filter(utilisateur=self.request.user).select_related('lieu')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        total = sum(f.lieu.cout for f in ctx['favoris'])
        ctx['total'] = total
        return ctx


class AddFavoriView(LoginRequiredMixin, View):
    """Ajoute un lieu aux favoris de l'utilisateur (POST uniquement)."""
    def post(self, request, pk):
        lieu = get_object_or_404(Lieu, pk=pk)
        favori, created = Favori.objects.get_or_create(
            utilisateur=request.user,
            lieu=lieu
        )
        if created:
            messages.success(request, f"✅ « {lieu.nom} » ajouté à votre plan !")
        else:
            messages.info(request, f"ℹ️ « {lieu.nom} » est déjà dans votre plan.")
        return redirect('lieux')


class RemoveFavoriView(LoginRequiredMixin, View):
    """Retire un lieu des favoris de l'utilisateur."""
    def post(self, request, pk):
        lieu = get_object_or_404(Lieu, pk=pk)
        deleted, _ = Favori.objects.filter(utilisateur=request.user, lieu=lieu).delete()
        if deleted:
            messages.success(request, f"🗑️ « {lieu.nom} » retiré de votre plan.")
        return redirect('favori_list')
