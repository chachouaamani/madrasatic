from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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

@login_required
def report_problem(request):
    if 'user_id' in request.session:
        user = get_user(request).pk
        data = Users.objects.get(pk=user)
    if request.method == "POST":
        titre = request.POST.get('titre')
        lieu = request.POST.get('lieu')
        salle = request.POST.get('salle')
        date = request.POST.get('date')
        desc = request.POST.get('description')
        heure = request.POST.get('heure')
        image = request.POST.get('image')
        valider = request.POST.get('valider')
        enregistrer = request.POST.get('enregistrer')

        if request.POST:
            cat_id = request.POST.get('selected_categorie')
        if (valider):
            if 'user_id' in request.session:
                user = get_user(request).pk


            signal = Signaux(user_id=user, titre=titre, category_id=cat_id, salle=salle, lieu=lieu, date=date,
                             heure=heure, send=True, description=desc)

            if len(request.FILES) != 0:
                signal.image = request.FILES['image']
            signal.save()
        if (enregistrer):
            if 'user_id' in request.session:
                user = get_user(request).pk

            signal = Signaux(user_id=user, titre=titre, category_id=cat_id, lieu=lieu, date=date, heure=heure,
                             image=image,
                             description=desc)
            if len(request.FILES) != 0:
                signal.image = request.FILES['image']
            signal.save()
            return redirect('categorie')

    context={
            'cat': Catégorie.objects.all(),
            'user':data

     }
    return render(request, "home_user/report_problem.html", context)

@login_required
def categorie(request):
    afficher_annonce = Annonce.objects.filter(validate=True)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)

    context = {'afficher_annonce': afficher_annonce,
               'categorie': Catégorie.objects.all(),
               'user':user

               }
    return render(request, "home_user/index.html", context)

@login_required
def signals(request, id):
    catname = Catégorie.objects.get(pk=id).name
    sig = Signaux.objects.filter(category__name=catname).filter(validate=True)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)

    context = {
        'sig': sig,
        'user':user

    }

    return render(request, "home_user/signals.html", context)

@login_required
def historique(request):
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)

    try:
      sig = Signaux.objects.filter(user_id=user_id)
    except Signaux.DoesNotExist:

      sig=None
    try:
       annonce = Annonce.objects.filter(user_id=user_id)
    except Annonce.DoesNotExist:
        annonce=None


    context = {
        'annonce': annonce,
        'sig': sig,
        'user': user
    }

    return render(request, "home_user/historique.html", context)

@login_required
def administration_club(request):
    afficher_annonce = Annonce.objects.filter(validate=True)
    categorie = Catégorie.objects.all()
    context = {'afficher_annonce': afficher_annonce,
               'categorie': categorie}

    return render(request, "home_user/administration&club.html", context)

@login_required
def add_announcement(request):
    if 'user_id' in request.session:
        user = get_user(request).pk
        data = Users.objects.get(pk=user)
    if request.method == "POST":

        Titre = request.POST.get("titre")
        Image = request.POST.get("image")
        Description = request.POST.get("description")
        Date_debut = request.POST.get("date_debut")
        Date_fin = request.POST.get("date_fin")
        save = request.POST.get("save")

        valider = request.POST.get("valider")
        if valider:
            if 'user_id' in request.session:
                user = get_user(request).pk


            annonce = Annonce(user_id=user, titre=Titre, description=Description, date_debut=Date_debut,
                              date_fin=Date_fin,send=True)

            if len(request.FILES) != 0:
                annonce.image = request.FILES['image']
            messages.success(request, "votre annonce est ajouté")

            annonce.save()

            return render(request, 'home_user/add_announcement.html')

        if save:
            if 'user_id' in request.session:
                user = get_user(request).pk

            annonce = Annonce(user_id=user, titre=Titre, description=Description, date_debut=Date_debut,
                              date_fin=Date_fin)

            if len(request.FILES) != 0:
                annonce.image = request.FILES['image']
            messages.success(request, "votre annonce est enregistrer")

            annonce.save()

            return render(request, 'home_user/add_announcement.html')



    return render(request, 'home_user/add_announcement.html',{'user':data})

@login_required
def signal_content(request, id):
    signal = Signaux.objects.get(pk=id)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)

    try:
        rapport = Rapport.objects.get(signalement_id=id)
    except Rapport.DoesNotExist:
        rapport = None

    context = {
        'signal': signal,
        'rapport': rapport,
        'user': user,
    }
    return render(request, 'home_user/signal_content.html', context)

@login_required
def annonce_content(request, id):
    annonce = Annonce.objects.get(pk=id)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)

    context = {
        'annonce': annonce,
        'user': user

    }
    return render(request, 'home_user/annonce_content.html', context)


@login_required
def signal_historique(request, id):
    signal = Signaux.objects.get(pk=id)


    context = {
        'signal': signal,
        'cat': Catégorie.objects.all(),

    }

    if request.method=="POST":
        cat_id = request.POST.get('selected_categorie')
        titre = request.POST.get('titre')
        lieu = request.POST.get('lieu')
        salle = request.POST.get('salle')
        date = request.POST.get('date')
        desc = request.POST.get('description')
        heure = request.POST.get('heure')
        delete = request.POST.get("delete")
        save = request.POST.get("save")
        signaler = request.POST.get("signaler")
        if delete:
            signal.delete()
            return redirect('historique')
        if signaler:
            signal.category_id=cat_id
            signal.titre=titre
            signal.lieu=lieu
            signal.salle=salle
            if len(date)!=0:
                signal.date = date

            signal.description=desc
            if len(heure)!=0:
                signal.heure = heure

            signal.send=True
            if len(request.FILES) != 0:
                signal.image = request.FILES['image']
            signal.save()
            return redirect('historique')

        if save:
            signal.category_id = cat_id
            signal.titre = titre
            signal.lieu = lieu
            signal.salle = salle
            if len(date) != 0:
                signal.date = date

            signal.description = desc
            if len(heure) != 0:
                signal.heure = heure

            if len(request.FILES) != 0:
                signal.image = request.FILES['image']
            signal.save()
            return redirect('historique')

    return render(request, 'home_user/sig_historique.html', context)

@login_required
def annonce_historique(request, id):
    annonce = Annonce.objects.get(pk=id)


    context = {
        'annonce': annonce,


    }

    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        date_debut = request.POST.get("date_debut")
        date_fin = request.POST.get("date_fin")
        delete = request.POST.get("delete")
        save = request.POST.get("save")
        valider= request.POST.get("valider")
        if delete:
            annonce.delete()
            return redirect('historique')
        if valider:

            annonce.send = True
            annonce.titre=titre
            annonce.description=description
            if len(date_fin)!=0 :
                annonce.date_fin = date_fin
            if len(date_debut)!=0:
                annonce.date_debut = date_debut

            annonce.save()
            return redirect('historique')

        if save:

            annonce.titre=titre
            annonce.description=description
            if len(date_fin)!=0 :
                annonce.date_fin = date_fin
            if len(date_debut)!=0:
                annonce.date_debut = date_debut

            annonce.save()
            return redirect('historique')
    return render(request, 'home_user/an_historique.html', context)

