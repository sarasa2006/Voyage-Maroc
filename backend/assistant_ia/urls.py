from django.urls import path
from .views import RecommandationView, ChatbotView

urlpatterns = [
    path('recommandation/', RecommandationView.as_view(), name='recommandation'),
    path('chat/', ChatbotView.as_view(), name='chatbot'),
]
