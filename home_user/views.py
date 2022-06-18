from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets

from users.models import Users
from .filters import OrderFilter
from .models import Signaux
from .models import Catégorie,Notifications,notify
from services.models import Rapport,Rapport_archivé

from django.contrib import messages
# Create your views here.
from home_user.models import Annonce
from rest_framework.response import Response
from rest_framework import status


from .serializers import SignauxSerializer
from rest_framework.decorators import api_view

@api_view (['GET','POST'])
def signaux_list (request):
    if request.method== 'GET':
        signaux=Signaux.objects.all()
        serializer=SignauxSerializer(signaux,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        serializer=SignauxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view (['GET','PUT','DELETE'])
def signaux_detail(request,id):
   try:
       sigaux=Signaux.objects.get(pk=id)
   except Signaux.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if request.method=='GET':

       serializer=SignauxSerializer(sigaux)
       return Response(serializer.data)

   elif request.method=='PUT':

       serialiser=SignauxSerializer(sigaux,data=request.data)
       if serialiser.is_valid():
           serialiser.save()
           return Response(serialiser.data)
       return Response(serialiser.error, status=status.HTTP_400_BAD_REQUEST)

   elif request.method =='DELETE':
       Signaux.delete()
       return Response(status=status.HTTP_204_NO_CONTENT)

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
            messages.add_message(request,messages.SUCCESS,"votre signalement  est ajouter")
            resp=Users.objects.get(role__name='responsable').pk
            message='un nouveau signalement est ajouté'
            notification=Notifications(to_user_id=resp,from_user_id=user,message=message,sig_id=signal.pk)
            notification.save()

            return redirect('historique')



        if (enregistrer):
            if 'user_id' in request.session:
                user = get_user(request).pk

            signal = Signaux(user_id=user, titre=titre, category_id=cat_id, lieu=lieu, date=date, heure=heure,
                             image=image,
                             description=desc)
            if len(request.FILES) != 0:
                signal.image = request.FILES['image']
            signal.save()
            messages.add_message(request, messages.SUCCESS, "votre signalement est enregistrer")
            return redirect('historique')
    notification = Notifications.objects.filter(to_user_id=user).order_by('-pk')
    annot=notify.objects.filter(to_user_id=user).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None
    context={
            'cat': Catégorie.objects.all(),
            'user':data,
             'notification':notification,
             'notif':annot

     }
    return render(request, "home_user/report_problem.html", context)

@login_required
def categorie(request):
    afficher_annonce = Annonce.objects.filter(validate=True)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)
        notification = Notifications.objects.filter(to_user_id=user_id).order_by('-pk')
        if request.method == "POST":
            sup = request.POST.get('sup')
            try:
                notif = Notifications.objects.get(pk=sup)
                notif.delete()
            except Notifications.DoesNotExist:
                notif=None


    context = {'afficher_annonce': afficher_annonce,
               'categorie': Catégorie.objects.all(),
               'user':user,
               'notification':notification,

               }
    return render(request, "home_user/index.html", context)

@login_required
def signals(request, id):
    catname = Catégorie.objects.get(pk=id).name
    sig = Signaux.objects.filter(category__name=catname).filter(validate=True)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)
        order_count=sig.count()

        myFilter = OrderFilter(request.GET,queryset=sig)
        sig=myFilter.qs
    if request.method=='POST':
        search=request.POST.get('search')
        sig=Signaux.objects.filter(category__name=catname).filter(validate=True).filter(titre__contains=search)|Signaux.objects.filter(category__name=catname).filter(validate=True).filter(description__contains=search)|Signaux.objects.filter(category__name=catname).filter(validate=True).filter(user__username__contains=search)|Signaux.objects.filter(category__name=catname).filter(validate=True).filter(lieu__contains=search)|Signaux.objects.filter(category__name=catname).filter(validate=True).filter(salle__contains=search)
    notification = Notifications.objects.filter(to_user_id=user_id).order_by('-pk')
    annot = notify.objects.filter(to_user_id=user_id).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None
    context = {
        'sig': sig,
        'user':user,
        'myFilter':myFilter,
        'order_count':order_count,
        'notification':notification,
        'notif':annot


    }

    return render(request, "home_user/signals.html", context)

@login_required
def historique(request):
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)

    try:
      sig = Signaux.objects.filter(user_id=user_id)


      order_count = sig.count()

      myFilter = OrderFilter(request.GET, queryset=sig)
      sig = myFilter.qs
    except Signaux.DoesNotExist:

      sig=None
    try:
       annonce = Annonce.objects.filter(user_id=user_id)
    except Annonce.DoesNotExist:
        annonce=None

    if request.method == 'POST':
        search = request.POST.get('search')
        sig = Signaux.objects.filter(user_id=user_id).filter(titre__contains=search) | Signaux.objects.filter(
            user_id=user_id).filter(description__contains=search) | Signaux.objects.filter(user_id=user_id).filter(
            salle__contains=search) | Signaux.objects.filter(user_id=user_id).filter(
            lieu__contains=search) | Signaux.objects.filter(user_id=user_id).filter(category__name__contains=search)
        annonce = Annonce.objects.filter(user_id=user_id).filter(titre__contains=search)| Annonce.objects.filter(user_id=user_id).filter(description__contains=search)

    notification = Notifications.objects.filter(to_user_id=user_id).order_by('-pk')
    annot = notify.objects.filter(to_user_id=user_id).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None

    context = {
        'annonce': annonce,
        'sig': sig,
        'user': user,
        'myFilter': myFilter,
        'order_count': order_count,
        'notification':notification,
        'notif':annot
    }

    return render(request, "home_user/historique.html", context)

@login_required
def administration_club(request):
    if 'user_id' in request.session:
        user_id = get_user(request).pk
    afficher_annonce = Annonce.objects.filter(validate=True)
    categorie = Catégorie.objects.all()

    notification = Notifications.objects.filter(to_user_id=user_id).order_by('-pk')
    annot = notify.objects.filter(to_user_id=user_id).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None
    context = {'afficher_annonce': afficher_annonce,
               'categorie': categorie,
               'notification':notification,
               'notif':annot
               }

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
            annonce.save()
            messages.add_message(request,messages.SUCCESS, "votre annonce est ajouté")
            resp = Users.objects.get(role__name='responsable').pk
            message = 'une nouvelle annonce est ajoutée'
            notification = notify(to_user_id=resp, from_user_id=user, message=message, an_id=annonce.pk)
            notification.save()

            return redirect('historique')

        if save:
            if 'user_id' in request.session:
                user = get_user(request).pk

            annonce = Annonce(user_id=user, titre=Titre, description=Description, date_debut=Date_debut,
                              date_fin=Date_fin)

            if len(request.FILES) != 0:
                annonce.image = request.FILES['image']
            annonce.save()
            messages.add_message(request, messages.SUCCESS, "votre annonce est enregistré")

            return redirect('historique')
    notification = Notifications.objects.filter(to_user_id=user).order_by('-pk')
    annot = notify.objects.filter(to_user_id=user).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None
    context={
        'user': data,
        'notification':notification,
        'notif':annot

    }


    return render(request, 'home_user/add_announcement.html',context)

@login_required
def signal_content(request, id):
    signal = Signaux.objects.get(pk=id)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)

    try:
        rapport = Rapport.objects.get(signalement_id=id,status='Traité')
    except Rapport.DoesNotExist:
        rapport = None

    notification = Notifications.objects.filter(to_user_id=user_id).order_by('-pk')
    annot = notify.objects.filter(to_user_id=user_id).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None
    context = {
        'signal': signal,
        'rapport': rapport,
        'user': user,
        'notification':notification,
        'notif':annot
    }
    return render(request, 'home_user/signal_content.html', context)

@login_required
def annonce_content(request, id):
    annonce = Annonce.objects.get(pk=id)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
        user = Users.objects.get(pk=user_id)

    notification = Notifications.objects.filter(to_user_id=user_id).order_by('-pk')
    annot = notify.objects.filter(to_user_id=user_id).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None
    context = {
        'annonce': annonce,
        'user': user,
        'notification':notification,
        'notif':annot

    }
    return render(request, 'home_user/annonce_content.html', context)


@login_required
def signal_historique(request, id):
    if 'user_id' in request.session:
        user_id = get_user(request).pk
    signal = Signaux.objects.get(pk=id)
    notification = Notifications.objects.filter(to_user_id=user_id).order_by('-pk')
    annot = notify.objects.filter(to_user_id=user_id).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None


    context = {
        'signal': signal,
        'cat': Catégorie.objects.all(),
        'notification':notification,
        'notif':annot

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
            messages.add_message(request,messages.ERROR,'signalement supprimé')
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
            messages.add_message(request, messages.SUCCESS, 'votre signalement est ajouté')
            resp = Users.objects.get(role__name='responsable').pk
            message = 'un nouveau signalement est ajouté'
            notification = Notifications(to_user_id=resp, from_user_id=signal.user.pk, message=message, sig_id=signal.pk)
            notification.save()
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
            messages.add_message(request, messages.SUCCESS, 'votre signalement est sauvgardé')
            return redirect('historique')

    return render(request, 'home_user/sig_historique.html', context)

@login_required
def annonce_historique(request, id):
    annonce = Annonce.objects.get(pk=id)
    if 'user_id' in request.session:
        user_id = get_user(request).pk
    notification = Notifications.objects.filter(to_user_id=user_id).order_by('-pk')
    annot = notify.objects.filter(to_user_id=user_id).order_by('-pk')
    if request.method == "POST":
        sup = request.POST.get('sup')
        try:
            notif = Notifications.objects.get(pk=sup)
            notif.delete()
        except Notifications.DoesNotExist:
            notif = None
        try:
            notiff = notify.objects.get(pk=sup)
            notiff.delete()
        except notify.DoesNotExist:
            notiff = None


    context = {
        'annonce': annonce,
        'notification':notification,
        'notif':annot


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
            messages.add_message(request, messages.ERROR, 'annonce est supprimé')
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
            messages.add_message(request, messages.SUCCESS, 'votre annonce est ajouté')
            if 'user_id' in request.session:
                user = get_user(request).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'une nouvelle annonce est ajoutée'
            notification = notify(to_user_id=resp, from_user_id=user, message=message, an_id=annonce.pk)
            notification.save()
            return redirect('historique')

        if save:

            annonce.titre=titre
            annonce.description=description
            if len(date_fin)!=0 :
                annonce.date_fin = date_fin
            if len(date_debut)!=0:
                annonce.date_debut = date_debut

            annonce.save()
            messages.add_message(request, messages.SUCCESS, 'votre signalement est sauvgardé')
            return redirect('historique')
    return render(request, 'home_user/an_historique.html', context)

