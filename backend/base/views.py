from django.views import View
from django.shortcuts import render
from voyages.models import Lieu

class HomeView(View):
    def get(self, request):
        villes_une = Lieu.objects.all()[:3]
        return render(request, 'base/home.html', {'villes_une': villes_une})