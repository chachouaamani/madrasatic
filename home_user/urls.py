from django.urls import path
from . import views



urlpatterns = [
path('report_problem/',views.report_problem,name="report_problem"),
path('signalements/<int:id>',views.signals,name="signals"),
path('historique/',views.historique,name="historique"),
path('home/',views.categorie,name="categorie"),

path('administration_club/',views.add_announcement,name="add_announcement"),
path('add_announcement/',views.add_announcement,name="add_announcement")  ,




]





