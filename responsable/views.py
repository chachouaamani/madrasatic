from django.shortcuts import render, redirect
from django.urls import reverse

from home_user.models import Signaux,Catégorie
from users.models import Users,Service
from django.contrib.auth.decorators import login_required


# Create your views here.
def category_table(request):
    category=Catégorie.objects.all()
    context={
        'category':category
    }
    return (request,'responsable/category_table.html',context)
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        save = request.POST.get('save')
        cancel=request.POST.get('cancel')
        if(save):
            category=Catégorie(name=name,description=description)
            if len(request.FILES) != 0:
                category.image = request.FILES['image']
            category.save()
            return redirect('category_table')
        if (cancel):
            return redirect('category_table')



    return render(request, 'responsable/add_category.html')

def category_manage(request,id):
    category=Catégorie.objects.get(pk=id)

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
            category.name=name
            category.description=description
            if len(request.FILES) != 0:
                category.image = request.FILES['image']
            category.save()
            return redirect('category_table')
        if (cancel):
            return redirect('category_table')

    return render(request,'responsable/category_manage.html')


def service_table(request):
    service = Service.objects.all()
    context = {
        'service': service
    }
    return (request, 'responsable/service_table.html', context)


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

    return render(request,'responsable/annonce.html')


def rapport(request):
    return render(request,'responsable/rapport.html')


def manage(request):

    declarations = Signaux.objects.all().order_by('-pk')

    context = {
        'declarations': declarations
    }
    return render(request, 'responsable/manage.html', context)


def content(request, id):
    declaration=Signaux.objects.get(pk=id)
    category=Catégorie.objects.all()
    service=Service.objects.all()

    context = {
        'declaration': declaration,
        'category': category,
        'service':service,
    }

    if request.method == "POST":
        categorie_id = request.POST.get("categorie")
        complement = request.POST.get("complement")
        service_send = request.POST.get("service")
        delete = request.POST.get("delete")
        rejeter=request.POST.get('rejeter')

        #declaration.category.id=categorie_id
        #declaration.complement=complement
        if (delete):
            declaration.delete()
            return redirect(reverse('manage'))
        if (service_send):
            declaration.validate = True
           # declaration.service_id=service
            declaration.save()
            return redirect(reverse('manage'))
        if(rejeter):
            declaration.statut="rejeter"
            declaration.save()
            return redirect(reverse('manage'))




    return render(request, 'responsable/content.html', context)
