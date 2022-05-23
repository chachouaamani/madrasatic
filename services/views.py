from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from home_user.filters import OrderFilter
from users.models import Users
from home_user.models import Signaux
from .models import Rapport


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

        context = {
            'rapport': rap,
            'user':service
        }
        return render(request, 'services/tab_rap.html', context)

@login_required
def service(request):
    if 'user_id' in request.session:
        user = get_user(request).role.service.name
        sig = Signaux.objects.filter(validate=True).filter(service__name=user)
        order_count = sig.count()

        myFilter = OrderFilter(request.GET, queryset=sig)
        sig = myFilter.qs
        if request.method == 'POST':
            search = request.POST.get('search')
            sig = Signaux.objects.filter(validate=True).filter(service__name=user).filter(titre__contains=search)|Signaux.objects.filter(validate=True).filter(service__name=user).filter(description__contains=search)|Signaux.objects.filter(validate=True).filter(service__name=user).filter(user__username__contains=search)|Signaux.objects.filter(validate=True).filter(service__name=user).filter(lieu__contains=search)|Signaux.objects.filter(validate=True).filter(service__name=user).filter(salle__contains=search)
        context = {
            'sig': sig,
            'user':user,
            'myFilter': myFilter,
            'order_count': order_count
        }
        return render(request, 'services/service.html', context)

@login_required
def add_rapport(request, id):
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
                              send=True)

            if len(request.FILES) != 0:
                rapport.image = request.FILES['image']
            messages.success(request, "votre rapport est validé")
            rapport.save()
            return redirect('rapport_service')

    return render(request, 'services/add_rapport.html')

@login_required
def view_rapport(request, id):
    rapport = Rapport.objects.get(pk=id)
    context = {
        'rapport': rapport
    }

    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        date = request.POST.get("date")
        save = request.POST.get('save')
        delete = request.POST.get('delete')
        valider = request.POST.get('valider')

        if (delete):
            rapport.delete()
            messages.add_message(request, messages.ERROR, "rapport est supprimé")
            return redirect('rapport_service')
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
            rapport.save()
            messages.add_message(request, messages.SUCCESS, "rapport envoyer")
            return redirect('rapport_service')

    return render(request, 'services/rapport.html', context)

@login_required
def signal_content(request, id):
    signal = Signaux.objects.get(pk=id)
    try:
        rapport = Rapport.objects.get(signalement_id=id)
    except Rapport.DoesNotExist:
        rapport = None

    context = {
        'signal': signal,
        'rapport': rapport,
    }
    if request.method == 'POST':
        valider = request.POST.get('valider')
        rejeter = request.POST.get('rejeter')
        if valider:
            signal.statut = 'Traité'
            signal.save()
            messages.add_message(request, messages.SUCCESS, 'signalement traité')
            return redirect('services')
        if rejeter:
            signal.validate=False
            signal.save()
            messages.add_message(request, messages.WARNING, 'signalement rejeté')
            return redirect('services')


    return render(request, 'services/signal.html', context)

@login_required
def content_rapport(request, id):
    rapport = Rapport.objects.get(pk=id)
    context = {
        'rapport': rapport,

    }

    return render(request, 'services/rapport_cont.html', context)
