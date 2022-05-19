from django.shortcuts import render, redirect
from django.urls import reverse

from home_user.models import Signaux, Catégorie, Annonce
from users.models import Users, Service
from services.models import Rapport
from django.contrib.auth.decorators import login_required


# Create your views here.
def category_table(request):
    category = Catégorie.objects.all()
    service = Service.objects.all()
    context = {
        'category': category,
        'service': service,
    }
    return render(request, 'responsable/category_table.html', context)


def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        save = request.POST.get('save')
        cancel = request.POST.get('cancel')
        if (save):
            category = Catégorie(name=name, description=description)
            if len(request.FILES) != 0:
                category.image = request.FILES['image']
            category.save()
            return redirect('category_table')
        if (cancel):
            return redirect('category_table')

    return render(request, 'responsable/add_category.html')


def category_manage(request, id):
    category = Catégorie.objects.get(pk=id)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        save = request.POST.get('save')
        delete = request.POST.get('delete')
        cancel = request.POST.get('cancel')

        if (delete):
            category.delete()
            return redirect('category_table')
        if (save):
            category.name = name
            category.description = description
            if len(request.FILES) != 0:
                category.image = request.FILES['image']
            category.save()
            return redirect('category_table')
        if (cancel):
            return redirect('category_table')

    return render(request, 'responsable/category_manage.html')



def add_service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        save = request.POST.get('save')
        cancel = request.POST.get('cancel')
        if (save):
            service = Service(name=name, description=description)
            service.save()
            return redirect('service_table')
        if (cancel):
            return redirect('service_table')

    return render(request, 'responsable/add_service.html')


def service_manage(request, id):
    service = Service.objects.get(pk=id)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        save = request.POST.get('save')
        delete = request.POST.get('delete')
        cancel = request.POST.get('cancel')

        if (delete):
            service.delete()
            return redirect('service_table')
        if (save):
            service.name = name
            service.description = description
            service.save()
            return redirect('service_table')
        if (cancel):
            return redirect('service_table')

    return render(request, 'responsable/service_manage.html')


def annonce(request):
    annonce = Annonce.objects.all()
    context = {
        'annonce': annonce

    }

    return render(request, 'responsable/annonce.html', context)


def rapport(request):
    rapport = Rapport.objects.all()
    context = {
        'rapport': rapport
    }
    return render(request, 'responsable/rapport.html', context)


def manage(request):
    declarations = Signaux.objects.all().order_by('-pk')

    context = {
        'declarations': declarations
    }
    return render(request, 'responsable/manage.html', context)


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
            declaration.save()
            return redirect(reverse('manage'))
        if (rejeter):
            declaration.statut = "Rejeter"
            declaration.save()
            return redirect(reverse('manage'))

    return render(request, 'responsable/content.html', context)

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
            return redirect(reverse('manage'))
        if (valider):
            rapport.validate = True
            rapport.status='Traité'
            rapport.save()
            return redirect(reverse('manage'))
        if (rejeter):
            rapport.status = "Rejeter"
            rapport.save()
            return redirect(reverse('manage'))

    return render(request, 'responsable/content_rapport.html', context)


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
            return redirect(reverse('manage'))
        if (valider):
            annonce.validate = True
            annonce.status='Traité'
            annonce.save()
            return redirect(reverse('manage'))
        if (rejeter):
            annonce.status = "Rejeter"
            annonce.save()
            return redirect(reverse('manage'))

    return render(request, 'responsable/content_annonce.html', context)

