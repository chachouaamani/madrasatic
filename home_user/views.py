from datetime import datetime

from django.shortcuts import render

from users.models import Users
from .models import Signaux
from .models import Catégorie
from services.models import Rapport


from django.contrib import messages
# Create your views here.
from home_user.models import Annonce




# Create your views here.

def get_user(request):
    return Users.objects.get(id=request.session['user_id'])
def report_problem (request):
 if request.method=="POST":
     titre=request.POST.get('titre')
     lieu=request.POST.get('lieu')
     salle=request.POST.get('salle')
     date=request.POST.get('date')
     desc=request.POST.get('description')
     heure=request.POST.get('heure')
     image=request.POST.get('image')
     valider=request.POST.get('valider')
     enregistrer=request.POST.get('enregistrer')


     if request.POST:
             cat_id=request.POST.get('selected_categorie')
     if(valider):
         if 'user_id' in request.session:
             user = get_user(request).pk

         signal=Signaux(user_id=user,titre=titre,category_id=cat_id,salle=salle,lieu=lieu,date=date,heure=heure,send=True,description=desc)

         if len(request.FILES)!=0:
             signal.image=request.FILES['image']
         signal.save()
     if(enregistrer):
         if 'user_id' in request.session:
             user = get_user(request).pk

         signal = Signaux(user_id=user,titre=titre, category_id=cat_id, lieu=lieu, date=date, heure=heure, image=image,
                          description=desc)
         if len(request.FILES) != 0:
             signal.image = request.FILES['image']
         signal.save()
 return render(request,"home_user/report_problem.html",{'cat':Catégorie.objects.all})

def categorie(request):

    afficher_annonce = Annonce.objects.filter(validate=True)



    context = {'afficher_annonce': afficher_annonce,
               'categorie':Catégorie.objects.all(),

               }
    return render(request, "home_user/index.html", context)





def signals(request,id):

     catname=Catégorie.objects.get(pk=id).name
     sig= Signaux.objects.filter(category__name=catname)


     context={
         'sig':sig,

     }



     return render(request, "home_user/signals.html",context)

def historique(request):
    return render(request,"home_user/historique.html")




def administration_club (request):

    afficher_annonce = Annonce.objects.filter(validate=True)
    context = {'afficher_annonce':afficher_annonce}

    return render(request,"home_user/administration&club.html",context)

def add_announcement (request):
 if request.method == "POST":

            Titre = request.POST.get("titre")
            Image=request.POST.get("image")
            Description = request.POST.get("description")
            Date_debut = request.POST.get("date_debut")
            Date_fin= request.POST.get("date_fin")

            if 'user_id' in request.session:
                user = get_user(request).pk

            annonce = Annonce(user_id=user,titre=Titre, description=Description ,date_debut=Date_debut,date_fin=Date_fin )

            if len (request.FILES) !=0:
                annonce.image=request.FILES['image']
            messages.success(request, "votre annonce est ajouté")

            annonce.save()






            return render(request, 'home_user/add_announcement.html')






 return render(request, 'home_user/add_announcement.html')



def signal_content(request,id):
    signal=Signaux.objects.get(pk=id)
    try:
        rapport = Rapport.objects.get(signalement_id=id)
    except Rapport.DoesNotExist:
        rapport = None

    context= {
        'signal':signal,
        'rapport':rapport,
    }
    return render(request,'home_user/signal_content.html',context)

def annonce_content(request,id):
    annonce=Annonce.objects.get(pk=id)

    context= {
        'annonce':annonce,

    }
    return render(request,'home_user/annonce_content.html',context)








