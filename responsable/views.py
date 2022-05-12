from django.shortcuts import render, redirect
from home_user.models import Signaux
from users.models import Users
from django.contrib.auth.decorators import login_required


# Create your views here.




def manage(request):

    declarations = Signaux.objects.all()

    context = {
        'declarations': declarations
    }
    return render(request, 'responsable/manage.html', context)


def content(request, id):
    declarations=Signaux.objects.get(pk=id)
    context = {
        'declarations': declarations
    }

    if request.method == "POST":
        categorie = request.POST.get("categorie")
        complement = request.POST.get("complement")
        service = request.POST.get("service")
        delete = request.POST.get("delete")

        declarations.category=categorie
        declarations.complement=complement
        if (delete):
            declarations.delete()
            return redirect('manage')
        if (service):
            declarations.validate = True
        declarations.save()


    return render(request, 'responsable/content.html', context)
