from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from home_user.filters import OrderFilter
from users.models import Users
from home_user.models import Signaux, Notifications
from .models import Rapport,notifyrapp


def get_user(request):
    return Users.objects.get(id=request.session['user_id'])

@login_required
def rapport(request):
    if 'user_id' in request.session:
        user = get_user(request).pk
        service=Users.objects.get(pk=user)
        rap = Rapport.objects.filter(user_id=user)
        if request.method=='POST':
            search=request.POST.get('search')
            rap = Rapport.objects.filter(user_id=user).filter(title__contains=search) | Rapport.objects.filter(user_id=user).filter(description__contains=search)
        cpt = Notifications.objects.filter(to_user_id=user).count() + notifyrapp.objects.filter(to_user_id=user).count()
        context = {
            'rapport': rap,
            'user':service,
            'cpt':cpt
        }
        return render(request, 'services/tab_rap.html', context)

@login_required
def service(request):
    if 'user_id' in request.session:
        user = get_user(request).role.service.name
        user_id=get_user(request).pk
        sig = Signaux.objects.filter(validate=True).filter(service__name=user)
        rapport=Rapport.objects.all()
        order_count = sig.count()

        myFilter = OrderFilter(request.GET, queryset=sig)
        sig = myFilter.qs
        if request.method == 'POST':
            search = request.POST.get('search')
            sig = Signaux.objects.filter(validate=True).filter(service__name=user).filter(titre__contains=search)|Signaux.objects.filter(validate=True).filter(service__name=user).filter(description__contains=search)|Signaux.objects.filter(validate=True).filter(service__name=user).filter(user__username__contains=search)|Signaux.objects.filter(validate=True).filter(service__name=user).filter(lieu__contains=search)|Signaux.objects.filter(validate=True).filter(service__name=user).filter(salle__contains=search)
        cpt = Notifications.objects.filter(to_user_id=user_id).count() + notifyrapp.objects.filter(to_user_id=user_id).count()
        context = {
            'sig': sig,
            'user':user,
            'myFilter': myFilter,
            'order_count': order_count,
            'rapport':rapport,
            'cpt':cpt
        }
        return render(request, 'services/service.html', context)

@login_required
def add_rapport(request, id):
    sig=Signaux.objects.get(pk=id)
    if request.method == "POST":

        Titre = request.POST.get("titre")
        Description = request.POST.get("description")
        Date = request.POST.get("date")
        btn1 = request.POST.get("save")
        btn2 = request.POST.get("valider")

        if btn1:
            if 'user_id' in request.session:
                user = get_user(request).pk

            rapport = Rapport(user_id=user, title=Titre, description=Description, date=Date, signalement_id=id)

            if len(request.FILES) != 0:
                rapport.image = request.FILES['image']
            messages.success(request, "votre rapport est enregistré")
            rapport.save()
            return redirect('rapport_service')
        if btn2:
            if 'user_id' in request.session:
                user = get_user(request).pk

            rapport = Rapport(user_id=user, title=Titre, description=Description, date=Date, signalement_id=id,
                              send=True,status='En_cours')


            if len(request.FILES) != 0:
                rapport.image = request.FILES['image']
            messages.success(request, "votre rapport est envoyé")
            rapport.save()
            sig.rapport_ajouter = True
            sig.save()
            resp = Users.objects.get(role__name='responsable').pk
            message = 'un nouveau rapport est ajouté'
            notification = notifyrapp(to_user_id=resp, from_user_id=user, message=message,
                                         rap_id=rapport.pk)
            notification.save()
            return redirect('rapport_service')

    return render(request, 'services/add_rapport.html')

@login_required
def view_rapport(request, id):
    rapport = Rapport.objects.get(pk=id)
    sig_id=rapport.signalement_id
    sig=Signaux.objects.get(pk=sig_id)
    if 'user_id' in request.session:
        user = get_user(request).pk

    context = {
        'rapport': rapport
    }

    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        date = request.POST.get("date")
        save = request.POST.get('save')
        valider = request.POST.get('valider')

        if (save):
            rapport.title = titre
            if len(date) != 0:
                rapport.date = date

            rapport.description = description
            rapport.save()
            messages.add_message(request, messages.SUCCESS, "modification sauvgardé")
            return redirect('rapport_service')
        if (valider):
            rapport.title = titre
            if len(date) != 0:
                rapport.date = date

            rapport.description = description
            rapport.send=True
            rapport.status='En_cours'
            rapport.save()
            sig.rapport_ajouter=True
            sig.save()
            resp = Users.objects.get(role__name='responsable').pk
            message = 'un nouveau rapport est ajouté'
            notification = notifyrapp(to_user_id=resp, from_user_id=user, message=message,
                                         rap_id=rapport.pk)
            notification.save()
            messages.add_message(request, messages.SUCCESS, "rapport envoyer")
            return redirect('rapport_service')

    return render(request, 'services/rapport.html', context)

@login_required
def signal_content(request, id):
    signal = Signaux.objects.get(pk=id)
    if 'user_id' in request.session:
        user = get_user(request).pk
    try:
        notificationn = Notifications.objects.get(sig_id=signal.pk, to_user=user)
        notificationn.delete()

    except Notifications.DoesNotExist:
        notificationn = None
    try:
        rapport = Rapport.objects.get(signalement_id=id,status='Traité')
    except Rapport.DoesNotExist:
        rapport = None

    context = {
        'signal': signal,
        'rapport': rapport,
    }



    return render(request, 'services/signal.html', context)

@login_required
def content_rapport(request, id):
    rapport = Rapport.objects.get(pk=id)
    if 'user_id' in request.session:
        user = get_user(request).pk
    try:
        notificationn = notifyrapp.objects.get(rap_id=rapport.pk, to_user=user)
        notificationn.delete()

    except notifyrapp.DoesNotExist:
        notificationn = None
    context = {
        'rapport': rapport,

    }

    return render(request, 'services/rapport_cont.html', context)


def notification(request):
    if 'user_id' in request.session:
        user = get_user(request).pk

    notification=Notifications.objects.filter(to_user_id=user)
    notif = notifyrapp.objects.filter(to_user_id=user)
    cpt = Notifications.objects.filter(to_user_id=user).count() + notifyrapp.objects.filter(to_user_id=user).count()


    context={
        'notification':notification,
        'notif':notif,
        'cpt':cpt
    }

    return render(request,'services/notification.html',context)