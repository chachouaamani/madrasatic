from datetime import datetime

from django.contrib import messages
from django.db.models import RestrictedError

from django.shortcuts import render, redirect
from django.urls import reverse


from home_user.filters import OrderFilter
from home_user.models import Signaux, Catégorie, Annonce,Notifications,Signaux_archivé
from users.models import Users, Service
from services.models import Rapport,Rapport_archivé
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def category_table(request):
    category = Catégorie.objects.all().order_by('-pk')
    service = Service.objects.all().order_by('-pk')

    if request.method=='POST':
        search=request.POST.get('search')
        category = Catégorie.objects.filter(name__contains=search) |  Catégorie.objects.filter(description__contains=search)
        service = Service.objects.filter(name__contains=search) | Service.objects.filter(description__contains=search)

    notification = Notifications.objects.filter(to_user__role__name='responsable').filter(has_seen=False).order_by( '-pk')
    context = {
        'category': category,
        'service': service,
        'notification':notification,
    }
    return render(request, 'responsable/category_table.html', context)

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
                return redirect('category_service')
            else:
                messages.add_message(request, messages.WARNING, "service est déjà exister!")
                return redirect('category_service')
        if (cancel):
            return redirect('category_service')

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
                return redirect('category_service')
            except RestrictedError:
                messages.add_message(request, messages.ERROR, "Vous pouvez pas supprimé ce service")
                return redirect('category_service')


        if (save):
            service.name = name
            service.description = description
            service.save()
            messages.add_message(request, messages.SUCCESS, "modification sauvgardé")
            return redirect('category_service')
        if (cancel):
            return redirect('category_service')

    return render(request, 'responsable/service_manage.html',context)

@login_required
def annonce(request):
    annonce = Annonce.objects.all().order_by('-pk')
    if request.method == 'POST':
        search = request.POST.get('search')
        annonce = Annonce.objects.filter(titre__contains=search)| Annonce.objects.filter(description__contains=search)| Annonce.objects.filter(user__username__contains=search)
    notification = Notifications.objects.filter(to_user__role__name='responsable').filter(has_seen=False).order_by('-pk')
    context = {
        'annonce': annonce,
        'notification':notification,

    }

    return render(request, 'responsable/annonce.html', context)

@login_required
def rapport(request):
    rapport = Rapport.objects.all().order_by('-pk')
    if request.method == 'POST':
        search = request.POST.get('search')
        rapport = Rapport.objects.filter(title__contains=search)| Rapport.objects.filter(description__contains=search)| Rapport.objects.filter(user__username__contains=search)
    notification = Notifications.objects.filter(to_user__role__name='responsable').filter(has_seen=False).order_by('-pk')
    context = {
        'rapport': rapport,
        'notification':notification,
    }
    return render(request, 'responsable/rapport.html', context)

@login_required
def manage(request):
    declarations = Signaux.objects.filter(send=True).order_by('-pk')
    notification=Notifications.objects.filter(to_user__role__name='responsable').filter(has_seen=False).order_by('-pk')
    cpt = Notifications.objects.filter(to_user__role__name='responsable').filter(has_seen=False).count()




    order_count = declarations.count()


    myFilter = OrderFilter(request.GET, queryset=declarations)
    declarations= myFilter.qs

    if request.method=='POST':
        search=request.POST.get('search')
        rech = request.POST.get('rech')
        if rech:
            declarations = Signaux.objects.filter(send=True).filter(titre__contains=search) | Signaux.objects.filter(
                send=True).filter(description__contains=search) | Signaux.objects.filter(send=True).filter(
                lieu__contains=search) | Signaux.objects.filter(send=True).filter(
                salle__contains=search) | Signaux.objects.filter(send=True).filter(
                category__name__contains=search) | Signaux.objects.filter(send=True).filter(
                user__username__contains=search)







    context = {
        'declarations': declarations,
        'myFilter': myFilter,
        'order_count': order_count,
        'notification':notification,
        'cpt':cpt,
    }

    return render(request, 'responsable/manage.html', context)

@login_required
def content_signal(request, id):
    declaration = Signaux.objects.get(pk=id)
    category = Catégorie.objects.all()
    service = Service.objects.all()


    context = {
        'declaration': declaration,
        'category': category,
        'service': service,

    }

    if request.method == "POST":
        categorie_id = request.POST.get("selected_categorie")
        service_id = request.POST.get("selected_service")
        archive = request.POST.get("archiver")
        rejeter = request.POST.get('rejeter')
        valider = request.POST.get('valider')
        save = request.POST.get('save')
        termine = request.POST.get('termine')

        if (save):
            declaration.category_id = categorie_id
            declaration.save()
        if (termine):
            declaration.statut='Traité'
            declaration.save()
            messages.add_message(request, messages.SUCCESS, 'signalement est marqué comme traité')
            return redirect(reverse('manage'))

        if (archive):
            declaration_archivé=Signaux_archivé(user_id=declaration.user_id, titre=declaration.titre, category_id=declaration.category_id, salle=declaration.salle, lieu=declaration.lieu, date=declaration.date,
                             heure=declaration.heure, send=declaration.send, description=declaration.description,image=declaration.image,statut=declaration.statut,validate=declaration.validate,service_id=declaration.service_id)
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
                rapport_archivé.save()
                declaration.delete()
                messages.add_message(request, messages.INFO, 'signalement est archivé')
                return redirect(reverse('manage'))





        if (valider):
            declaration.service_id = service_id
            declaration.validate = True
            declaration.statut='En_cours'
            declaration.save()
            messages.add_message(request, messages.SUCCESS, 'signalement est envoyer à service ')
            user = Users.objects.get(pk=declaration.user.pk).pk
            resp = Users.objects.get(role__name='responsable').pk
            message = 'votre signalement est validé'
            notification = Notifications(to_user_id=user, from_user_id=resp, message=message, sig_id=declaration.pk)
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
    context = {
        'rapport': rapport,

    }

    if request.method == "POST":

        rejeter = request.POST.get('rejeter')
        valider = request.POST.get('valider')

        if (valider):
            rapport.validate = True
            rapport.status='Traité'
            rapport.save()
            messages.add_message(request, messages.SUCCESS, 'rapport est validé')
            return redirect(reverse('rapport'))
        if (rejeter):
            rapport.status = "Rejeté"
            rapport.save()
            messages.add_message(request, messages.WARNING, 'rapport est rejeté')
            return redirect(reverse('rapport'))

    return render(request, 'responsable/content_rapport.html', context)

@login_required
def content_annonce(request, id):
    annonce = Annonce.objects.get(pk=id)

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
            return redirect(reverse('annonce'))
        if (rejeter):
            annonce.status = "Rejeté"
            annonce.save()
            messages.add_message(request, messages.WARNING, 'annonce est rejeté')
            return redirect(reverse('annonce'))

    return render(request, 'responsable/content_annonce.html', context)

@login_required
def test(request):
    sj = Signaux.objects.filter(date__month=1).count()
    sf = Signaux.objects.filter(date__month=2).count()
    sa = Signaux.objects.filter(date__month=4).count()
    sm = Signaux.objects.filter(date__month=5).count()

    si = Signaux.objects.filter(category__pk=1).count()
    signa = Signaux.objects.filter(category__pk=2).count()
    ct = Catégorie.objects.all()

    sigt = 0
    sigtt=0
    for i in range(1, si + 1):
        diff = Signaux.objects.get(category__pk=1, pk=i).date
        d = datetime.now().date().day - diff.day
        sigt = sigt + d / si
    for j in range(si+1,signa+1):
        diff=Signaux.objects.get(category__pk=2, pk=j).date
        d = datetime.now().date().day - diff.day
        sigtt = sigtt + d / signa+1


    context = {
        'signa': signa,
        'si': si,
        'ct': ct,
        'sj': sj, 'sf': sf, 'sm': sm, 'sa': sa,
        'sigt': sigt,
        'sigtt':sigtt,
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
    return render(request, 'responsable/content_signal_archive.html', context)

@login_required
def archive(request):
    declarations = Signaux_archivé.objects.all().order_by('-pk')


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

    }

    return render(request, 'responsable/signal_archive.html', context)

def notification(request):
    return render(request,'responsable/notification.html')