from django.shortcuts import render
from .models import Declaration
from users.models import Users


# Create your views here.

def declaration(request):
    if request.method == "POST":
        titre = request.POST.get("title")
        description = request.POST.get("description")
        categorie = request.POST.get("categorie")
        image = request.POST.get("image")
        date = request.POST.get("date")
        place = request.POST.get("place")
        declaration = Declaration(User_id="1",title=titre, description=description, category=categorie, date=date,
                                  place=place)
        if len(request.FILES) != 0:
            declaration.image=request.FILES['image']
        declaration.save()

    return render(request, "responsable/declaration.html")


def manage(request):

    declarations=Declaration.objects.all()

    context={
        'declarations':declarations
    }
    return render(request, 'responsable/manage.html',context)
