from datetime import datetime

from django.contrib import messages
from django.db.models import RestrictedError

from django.shortcuts import render, redirect
from django.urls import reverse


from home_user.filters import OrderFilter
from home_user.models import Signaux, Catégorie, Annonce, Notifications, Signaux_archivé, notify
from users.models import Users, Service
from services.models import Rapport,Rapport_archivé,notifyrapp
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def category_table(request):
    category = Catégorie.objects.all().order_by('-pk')


    cpt1 = Notifications.objects.filter(to_user__role__name='responsable').count()
    cpt2 = notify.objects.filter(to_user__role__name='responsable').count()
    cpt3 = notifyrapp.objects.filter(to_user__role__name='responsable').count()
    cpt=cpt1+cpt2+cpt3


    if request.method=='POST':
        search=request.POST.get('search')
        category = Catégorie.objects.filter(name__contains=search) |  Catégorie.objects.filter(description__contains=search)



    context = {
        'category': category,
        'cpt':cpt

    }
    return render(request, 'responsable/category_table.html', context)


@login_required
def service_table(request):

    service = Service.objects.all().order_by('-pk')

    cpt1 = Notifications.objects.filter(to_user__role__name='responsable').count()
    cpt2 = notify.objects.filter(to_user__role__name='responsable').count()
    cpt3 = notifyrapp.objects.filter(to_user__role__name='responsable').count()
    cpt=cpt1+cpt2+cpt3


    if request.method=='POST':
        search=request.POST.get('search')

        service = Service.objects.filter(name__contains=search) | Service.objects.filter(description__contains=search)


    context = {

        'service': service,
        'cpt':cpt

    }
    return render(request, 'responsable/service_table.html', context)

@login_required
def add_category(request):
    ser = Service.objects.all()
    if request.method == "POST":

        name = request.POST.get("titre")
        service = request.POST.get("selected_service")
        description = request.POST.get("description")
        save = request.POST.get('save')
        cancel = request.POST.get('cancel')

        if (save):
            if not Catégorie.objects.filter(name=name).exists():
                category = Catégorie(name=name, description=description,service_id=service)
                if len(request.FILES) != 0:
                    category.image = request.FILES['image']
                category.save()
                messages.add_message(request, messages.SUCCESS, "categorie est ajouter")
                return redirect('category_service')
            else:
                messages.add_message(request, messages.WARNING, "categorie est déjà exister!")
                return redirect('category_service')
        if (cancel):
            return redirect('category_service')
    context = {
        'ser': ser
    }
    return render(request, 'responsable/add_category.html',context)

@login_required
def category_manage(request, id):
    category = Catégorie.objects.get(pk=id)
    ser=Service.objects.all()
    context={
        'category':category,
        'ser':ser
    }

    if request.method == "POST":
        service = request.POST.get("selected_service")
        name = request.POST.get("titre")
        description = request.POST.get("description")
        save = request.POST.get('save')
        delete = request.POST.get('delete')
        cancel = request.POST.get('cancel')

        if (delete):
            try :
                category.delete()
                messages.add_message(request, messages.ERROR, "catégorie est supprimé")
                return redirect('category_service')
            except RestrictedError :
                messages.add_message(request, messages.ERROR, "vous pouvez pas supprimé cette categorie car elle contient des signalements")
                return redirect('category_service')

        if (save):
            category.name = name
            category.service_id=service
            category.description = description
            if len(request.FILES) != 0:
                category.image = request.FILES['image']
            category.save()
            messages.add_message(request, messages.SUCCESS, "modification sauvgardé")
            return redirect('category_service')

        if (cancel):
            return redirect('category_service')

    return render(request, 'responsable/category_manage.html',context)


@login_required
def add_service(request):
    if request.method == "POST":
        name = request.POST.get("titre")
        description = request.POST.get("description")
        save = request.POST.get('save')
        cancel = request.POST.get('cancel')
        if (save):
            if not Service.objects.filter(name=name).exists():
                service = Service(name=name, description=description)
                service.save()
                messages.add_message(request, messages.SUCCESS, "service est ajouter")
                return redirect('service_table')
            else:
                messages.add_message(request, messages.WARNING, "service est déjà exister!")
                return redirect('service_table')
        if (cancel):
            return redirect('service_table')

    return render(request, 'responsable/add_service.html')

@login_required
def service_manage(request, id):
    service = Service.objects.get(pk=id)
    context={
        'service':service
    }

    if request.method == "POST":
        name = request.POST.get("titre")
        description = request.POST.get("description")
        save = request.POST.get('save')
        delete = request.POST.get('delete')
        cancel = request.POST.get('cancel')

        if (delete):
            try :
                service.delete()
                messages.add_message(request, messages.ERROR, "service est supprimé")
                return redirect('service_table')
            except RestrictedError:
                messages.add_message(request, messages.ERROR, "Vous pouvez pas supprimé ce service")
                return redirect('service_table')


        if (save):
            service.name = name
            service.description = description
            service.save()
            messages.add_message(request, messages.SUCCESS, "modification sauvgardé")
            return redirect('service_table')
        if (cancel):
            return redirect('service_table')

    return render(request, 'responsable/service_manage.html',context)

@login_required
def annonce(request):
    annonce = Annonce.objects.filter(send=True).order_by('-pk')
    if request.method == 'POST':
        search = request.POST.get('search')
        annonce = Annonce.objects.filter(send=True).filter(titre__contains=search)| Annonce.objects.filter(send=True).filter(description__contains=search)| Annonce.objects.filter(send=True).filter(user__username__contains=search)
    cpt1 = Notifications.objects.filter(to_user__role__name='responsable').count()
    cpt2 = notify.objects.filter(to_user__role__name='responsable').count()
    cpt3 = notifyrapp.objects.filter(to_user__role__name='responsable').count()
    cpt = cpt1 + cpt2 + cpt3
    context = {
        'annonce': annonce,
        'cpt':cpt,


    }

    return render(request, 'responsable/annonce.html', context)

@login_required
def rapport(request):
    rapport = Rapport.objects.filter(send=True).order_by('-pk')

    if request.method == 'POST':
        search = request.POST.get('search')
        rapport = Rapport.objects.filter(send=True).filter(title__contains=search)| Rapport.objects.filter(send=True).filter(description__contains=search)| Rapport.objects.filter(send=True).filter(user__username__contains=search)
    cpt1 = Notifications.objects.filter(to_user__role__name='responsable').count()
    cpt2 = notify.objects.filter(to_user__role__name='responsable').count()
    cpt3 = notifyrapp.objects.filter(to_user__role__name='responsable').count()
    cpt = cpt1 + cpt2 + cpt3
    context = {
        'rapport': rapport,
        'cpt':cpt
    }
    return render(request, 'responsable/rapport.html', context)

@login_required
def manage(request):
    declarations = Signaux.objects.filter(send=True).filter(rattacher=False).order_by('-pk')
    cpt1 = Notifications.objects.filter(to_user__role__name='responsable').count()
    cpt2 = notify.objects.filter(to_user__role__name='responsable').count()
    cpt3 = notifyrapp.objects.filter(to_user__role__name='responsable').count()
    cpt = cpt1 + cpt2 + cpt3




    order_count = declarations.count()


    myFilter = OrderFilter(request.GET, queryset=declarations)
    declarations= myFilter.qs

    if request.method=='POST':
        search=request.POST.get('search')
        rech = request.POST.get('rech')
        if rech:
            declarations = Signaux.objects.filter(send=True).filter(rattacher=False).filter(titre__contains=search) | Signaux.objects.filter(
                send=True).filter(rattacher=False).filter(description__contains=search) | Signaux.objects.filter(send=True).filter(rattacher=False).filter(
                lieu__contains=search) | Signaux.objects.filter(send=True).filter(rattacher=False).filter(
                salle__contains=search) | Signaux.objects.filter(send=True).filter(rattacher=False).filter(
                category__name__contains=search) | Signaux.objects.filter(send=True).filter(rattacher=False).filter(
                user__username__contains=search)


    if request.method == 'POST':
        rattacher = request.POST.get('rattacher')

        if rattacher:
            id_list=request.POST.getlist('boxes')
            for x in id_list:
                if int(x)!=int(rattacher):
                    Signaux.objects.filter(pk=int(x)).update(rattacher=True, pere=int(rattacher))


    context = {
        'declarations': declarations,
        'myFilter': myFilter,
        'order_count': order_count,
        'cpt':cpt,
    }

    return render(request, 'responsable/manage.html', context)

@login_required
def content_signal(request, id):
    declaration = Signaux.objects.get(pk=id)
    category = Catégorie.objects.all()

    try:
        notification = Notifications.objects.get(sig_id=declaration.pk, to_user__role__name='responsable')
        notification.delete()

    except Notifications.DoesNotExist:
       notification=None
    context = {
        'declaration': declaration,
        'category': category,


    }

    if request.method == "POST":
        categorie_id = request.POST.get("selected_categorie")
        archive = request.POST.get("archiver")
        rejeter = request.POST.get('rejeter')
        valider = request.POST.get('valider')
        save = request.POST.get('save')


        if (save):
            declaration.category_id = categorie_id
            declaration.save()


        if (archive):
            declaration_archivé=Signaux_archivé(user_id=declaration.user_id, titre=declaration.titre, category_id=declaration.category_id, salle=declaration.salle, lieu=declaration.lieu, date=declaration.date,
                             heure=declaration.heure, send=declaration.send, description=declaration.description,image=declaration.image,statut=declaration.statut,validate=declaration.validate,service_id=declaration.service_id,rapport_ajouter=declaration.rapport_ajouter,pere=declaration.pere,rattacher=declaration.rattacher)
            declaration_archivé.save()
            try:
                rapport = Rapport.objects.get(signalement_id=declaration.pk)
                rapport_archivé=Rapport_archivé(user_id=rapport.user.pk, title=rapport.title, description=rapport.description, date=rapport.date, signalement_id=declaration_archivé.pk,
                              send=rapport.send,status=rapport.status)
                rapport_archivé.save()
                declaration.delete()
                messages.add_message(request, messages.INFO, 'signalement est archivé')
                return redirect(reverse('manage'))

            except Rapport.DoesNotExist as e:
                declaration.delete()
                messages.add_message(request, messages.INFO, 'signalement est archivé')
                return redirect(reverse('manage'))





        if (valider):
            service_id=Catégorie.objects.get(pk=categorie_id).service_id
            declaration.service_id=service_id
            declaration.validate = True
            declaration.statut='En_cours'
            declaration.save()
            messages.add_message(request, messages.SUCCESS, 'signalement est envoyer à service ')
            user = Users.objects.get(pk=declaration.user.pk).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'votre signalement est validé'
            notificationn = Notifications(to_user_id=user, from_user_id=resp, message=message, sig_id=declaration.pk)
            notificationn.save()
            userr = Users.objects.get(role__service_id=service_id).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'un nouveau signalement est reçus'
            notification = Notifications(to_user_id=userr, from_user_id=resp, message=message, sig_id=declaration.pk)
            notification.save()
            return redirect(reverse('manage'))
        if (rejeter):
            declaration.statut = "Rejeté"
            declaration.save()
            messages.add_message(request, messages.WARNING, 'signalement est rejeté')
            user = Users.objects.get(pk=declaration.user.pk).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'votre signalement est rejeté'
            notification = Notifications(to_user_id=user, from_user_id=resp, message=message, sig_id=declaration.pk)
            notification.save()
            return redirect(reverse('manage'))

    return render(request, 'responsable/content.html', context)
@login_required
def content_rapport(request, id):
    rapport = Rapport.objects.get(pk=id)
    try:
        notification = notifyrapp.objects.get(rap_id=rapport.pk, to_user__role__name='responsable')
        notification.delete()

    except notifyrapp.DoesNotExist:
        notification = None

    context = {
        'rapport': rapport,

    }

    if request.method == "POST":

        rejeter = request.POST.get('rejeter')
        valider = request.POST.get('valider')

        if (valider):
            declaration=Signaux.objects.get(pk=rapport.signalement_id)
            declaration.statut="Traité"
            declaration.save()
            user = Users.objects.get(pk=rapport.signalement.user_id).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'votre signalement est traité'
            notification = Notifications(to_user_id=user, from_user_id=resp, message=message,
                                         sig_id=rapport.signalement.pk)
            notification.save()
            rapport.validate = True
            rapport.status='Traité'
            rapport.save()
            messages.add_message(request, messages.SUCCESS, 'rapport est validé')
            user = Users.objects.get(pk=rapport.user.pk).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'votre rapport est validé'
            notification = Notifications(to_user_id=user, from_user_id=resp, message=message, sig_id=rapport.signalement.pk)
            notification.save()
            return redirect(reverse('rapport'))
        if (rejeter):
            rapport.status = "Rejeté"
            rapport.save()
            messages.add_message(request, messages.WARNING, 'rapport est rejeté')
            user = Users.objects.get(pk=rapport.user.pk).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'votre rapport est rejeté'
            notification = Notifications(to_user_id=user, from_user_id=resp, message=message,
                                         sig_id=rapport.signalement.pk)
            notification.save()

            return redirect(reverse('rapport'))

    return render(request, 'responsable/content_rapport.html', context)

@login_required
def content_annonce(request, id):
    annonce = Annonce.objects.get(pk=id)
    try:
        notification = notify.objects.get(an_id=annonce.pk, to_user__role__name='responsable')
        notification.delete()

    except notify.DoesNotExist:
        notification = None

    context = {
        'annonce': annonce,

    }

    if request.method == "POST":
        rejeter = request.POST.get('rejeter')
        valider = request.POST.get('valider')


        if (valider):
            annonce.validate = True
            annonce.status='Traité'
            annonce.save()
            messages.add_message(request, messages.SUCCESS, 'annonce est validé')
            user = Users.objects.get(pk=annonce.user.pk).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'votre annonce est validé'
            notification = notify(to_user_id=user, from_user_id=resp, message=message,
                                         an_id=annonce.pk)
            notification.save()



            return redirect(reverse('annonce'))
        if (rejeter):
            annonce.status = "Rejeté"
            annonce.save()
            messages.add_message(request, messages.WARNING, 'annonce est rejeté')
            user = Users.objects.get(pk=annonce.user.pk).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'votre annonce est rejeté'
            notification = notify(to_user_id=user, from_user_id=resp, message=message,
                                  an_id=annonce.pk)
            notification.save()
            return redirect(reverse('annonce'))

    return render(request, 'responsable/content_annonce.html', context)

@login_required
def test(request):
    #les notification
    cpt1 = Notifications.objects.filter(to_user__role__name='responsable').count()
    cpt2 = notify.objects.filter(to_user__role__name='responsable').count()
    cpt3 = notifyrapp.objects.filter(to_user__role__name='responsable').count()
    cpt = cpt1 + cpt2 + cpt3
    #####
    sj = Signaux.objects.filter(date__month=1).count()
    sf = Signaux.objects.filter(date__month=2).count()
    sms = Signaux.objects.filter(date__month=3).count()
    sa = Signaux.objects.filter(date__month=4).count()
    sm = Signaux.objects.filter(date__month=5).count()
    sju = Signaux.objects.filter(date__month=6).count()
    sjj = Signaux.objects.filter(date__month=7).count()
    sout = Signaux.objects.filter(date__month=8).count()
    ssp = Signaux.objects.filter(date__month=9).count()
    soc = Signaux.objects.filter(date__month=10).count()
    snv = Signaux.objects.filter(date__month=11).count()
    sdc = Signaux.objects.filter(date__month=12).count()

    ct = Catégorie.objects.all()

    # le nombre des cat
    x = 1
    sigs = 0
    sigss = []
    liste = []
    list_id=[]
    list_id=Catégorie.objects.values_list('id',flat=True)
    print(list_id)
    nb_cat=Catégorie.objects.all().count()

    for i in list_id:
        sig = Signaux.objects.filter(category_id=i).count()
        liste.append(sig)
        for j in range(x, sig + x):
            try:
                if (Signaux.objects.get(category__pk=i, pk=j).statut == 'Traité'):
                    diff = Signaux.objects.get(category__pk=i, pk=j).date
                    try:
                        d = Rapport.objects.get(signalement__pk=j).date - diff
                        sigs = sigs + d.days / sig
                    except Rapport.DoesNotExist:
                        sigs = 0

                    sigss.append(sigs)
                    sigs = 0
                else:
                    diff = 0
            except Signaux.DoesNotExist:
                diff = 0

        x = sig + x

    context = {
        'liste': liste,
        'sj': sj, 'sf': sf, 'sm': sm, 'sa': sa, 'sms': sms, 'sju': sju, 'sjj': sjj, 'sout': sout, 'ssp': ssp,
        'soc': soc, 'snv': snv,
        'sdc': sdc,
        'sigs': sigss,
        'ct': ct,
        # les notification
        'cpt': cpt
    }

    return render(request, 'responsable/statistic.html', context)


@login_required
def content_signal_archivé(request, id):
    signal = Signaux_archivé.objects.get(pk=id)

    try:
        rapport = Rapport_archivé.objects.get(signalement_id=signal.pk)
    except Rapport_archivé.DoesNotExist:
        rapport = None

    context = {
        'signal': signal,
        'rapport': rapport,

    }
    if request.method=='POST':
        restaurer=request.POST.get('restaurer')
        if restaurer:
            declaration_restaurer = Signaux(user_id=signal.user_id, titre=signal.titre,
                                                  category_id=signal.category_id, salle=signal.salle,
                                                  lieu=signal.lieu, date=signal.date,
                                                  heure=signal.heure, send=signal.send,
                                                  description=signal.description, image=signal.image,
                                                  statut=signal.statut, validate=signal.validate,
                                                  service_id=signal.service_id,
                                                  rapport_ajouter=signal.rapport_ajouter, pere=signal.pere,
                                                  rattacher=signal.rattacher)
            declaration_restaurer.save()
            try:
                rapportt = Rapport_archivé.objects.get(signalement_id=signal.pk)
                rapport_restaurer = Rapport(user_id=rapportt.user.pk, title=rapportt.title,
                                                  description=rapportt.description, date=rapportt.date,
                                                  signalement_id=declaration_restaurer.pk,
                                                  send=rapportt.send, status=rapportt.status)
                rapport_restaurer.save()
                signal.delete()
                messages.add_message(request, messages.INFO, 'signalement est restauré')
                return redirect(reverse('archive'))

            except Rapport_archivé.DoesNotExist as e:
                signal.delete()
                messages.add_message(request, messages.INFO, 'signalement est restauré')
                return redirect(reverse('archive'))
    return render(request, 'responsable/content_signal_archive.html', context)

@login_required
def archive(request):
    declarations = Signaux_archivé.objects.all().order_by('-pk')
    cpt1 = Notifications.objects.filter(to_user__role__name='responsable').count()
    cpt2 = notify.objects.filter(to_user__role__name='responsable').count()
    cpt3 = notifyrapp.objects.filter(to_user__role__name='responsable').count()
    cpt = cpt1 + cpt2 + cpt3

    if request.method == 'POST':
        search = request.POST.get('search')
        rech = request.POST.get('rech')
        if rech:
            declarations = Signaux_archivé.objects.filter(titre__contains=search) | Signaux_archivé.objects.filter(description__contains=search) | Signaux_archivé.objects.filter(
                lieu__contains=search) | Signaux_archivé.objects.filter(
                salle__contains=search) | Signaux_archivé.objects.filter(
                category__name__contains=search) | Signaux_archivé.objects.filter(
                user__username__contains=search)

    context = {
        'declarations': declarations,
        'cpt':cpt

    }

    return render(request, 'responsable/signal_archive.html', context)

def notification(request):

    notification=Notifications.objects.filter(to_user__role__name='responsable')
    notifrap=notifyrapp.objects.filter(to_user__role__name='responsable')
    notifan=notify.objects.filter(to_user__role__name='responsable')
    cpt1 = Notifications.objects.filter(to_user__role__name='responsable').count()
    cpt2 = notify.objects.filter(to_user__role__name='responsable').count()
    cpt3 = notifyrapp.objects.filter(to_user__role__name='responsable').count()
    cpt = cpt1 + cpt2 + cpt3


    context={
        'notif':notifrap,
        'noti':notifan,
        'notification':notification,
        'cpt':cpt
    }

    return render(request,'responsable/notification.html',context)

