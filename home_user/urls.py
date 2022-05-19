from django.urls import path
from . import views



urlpatterns = [
path('report_problem/',views.report_problem,name="report_problem"),
path('signalements/<int:id>',views.signals,name="signals"),
path('historique/',views.historique,name="historique"),
path('home/',views.categorie,name="categorie"),
path('signal_contenu/<int:id>',views.signal_content,name="signal_content"),
path('annonce_contenu/<int:id>',views.annonce_content,name="annonce_content"),
path('administration_club/',views.administration_club,name="administration"),
path('add_announcement/',views.add_announcement,name="add_announcement")  ,




]





