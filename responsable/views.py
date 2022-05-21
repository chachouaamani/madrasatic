from datetime import datetime

from django.contrib import messages

from django.shortcuts import render, redirect
from django.urls import reverse

from home_user.models import Signaux, Catégorie, Annonce
from users.models import Users, Service
from services.models import Rapport
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def category_table(request):
    category = Catégorie.objects.all()
    service = Service.objects.all()
    context = {
        'category': category,
        'service': service,
    }
    return render(request, 'responsable/category_table.html', context)

@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("titre")
        description = request.POST.get("description")
        save = request.POST.get('save')
        cancel = request.POST.get('cancel')
        if (save):
            if not Catégorie.objects.filter(name=name).exists():
                category = Catégorie(name=name, description=description)
                if len(request.FILES) != 0:
                    category.image = request.FILES['image']
                category.save()
                messages.add_message(request, messages.SUCCESS, "categorie est ajouter")
                return redirect('category_service')
            else:
                messages.add_message(request, messages.INFO, "categorie est déjà exister!")
                return redirect('category_service')
        if (cancel):
            return redirect('category_service')

    return render(request, 'responsable/add_category.html')

@login_required
def category_manage(request, id):
    category = Catégorie.objects.get(pk=id)
    context={
        'category':category
    }

    if request.method == "POST":
        name = request.POST.get("titre")
        description = request.POST.get("description")
        save = request.POST.get('save')
        delete = request.POST.get('delete')
        cancel = request.POST.get('cancel')

        if (delete):
            category.delete()
            messages.add_message(request, messages.ERROR, "catégorie est supprimé")
            return redirect('category_service')
        if (save):
            category.name = name
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
                messages.add_message(request, messages.INFO, "service est déjà exister!")
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
            service.delete()
            messages.add_message(request, messages.ERROR, "service est supprimé")
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
    annonce = Annonce.objects.all()
    context = {
        'annonce': annonce

    }

    return render(request, 'responsable/annonce.html', context)

@login_required
def rapport(request):
    rapport = Rapport.objects.all()
    context = {
        'rapport': rapport
    }
    return render(request, 'responsable/rapport.html', context)

@login_required
def manage(request):
    declarations = Signaux.objects.filter(send=True).order_by('-pk')

    context = {
        'declarations': declarations
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
        complement = request.POST.get("complement")
        service_id = request.POST.get("selected_service")
        delete = request.POST.get("delete")
        rejeter = request.POST.get('rejeter')
        valider = request.POST.get('valider')
        save = request.POST.get('save')

        if (save):
            declaration.category_id = categorie_id
            declaration.save()

        # declaration.complement=complement
        if (delete):
            declaration.delete()
            return redirect(reverse('manage'))
        if (valider):
            declaration.service_id = service_id
            declaration.validate = True
            declaration.statut='En_cours'
            declaration.save()
            return redirect(reverse('manage'))
        if (rejeter):
            declaration.statut = "Rejeter"
            declaration.save()
            return redirect(reverse('manage'))

    return render(request, 'responsable/content.html', context)
@login_required
def content_rapport(request, id):
    rapport = Rapport.objects.get(pk=id)
    context = {
        'rapport': rapport,

    }

    if request.method == "POST":
        delete = request.POST.get("delete")
        rejeter = request.POST.get('rejeter')
        valider = request.POST.get('valider')

        if (delete):
            rapport.delete()
            return redirect(reverse('rapport'))
        if (valider):
            rapport.validate = True
            rapport.status='Traité'
            rapport.save()
            return redirect(reverse('rapport'))
        if (rejeter):
            rapport.status = "Rejeter"
            rapport.save()
            return redirect(reverse('rapport'))

    return render(request, 'responsable/content_rapport.html', context)

@login_required
def content_annonce(request, id):
    annonce = Annonce.objects.get(pk=id)

    context = {
        'annonce': annonce,

    }

    if request.method == "POST":
        delete = request.POST.get("delete")
        rejeter = request.POST.get('rejeter')
        valider = request.POST.get('valider')


        if (delete):
            annonce.delete()
            return redirect(reverse('annonce'))
        if (valider):
            annonce.validate = True
            annonce.status='Traité'
            annonce.save()
            return redirect(reverse('annonce'))
        if (rejeter):
            annonce.status = "Rejeter"
            annonce.save()
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
