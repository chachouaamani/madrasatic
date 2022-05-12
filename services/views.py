from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from users.models import Users
from home_user.models import Signaux
from .forms import UserUpdateForm


def get_user(request):
    return Users.objects.get(id=request.session['user_id'])


def services(request):
    if 'user_id' in request.session:
      user = get_user(request)
      if user.is_service == True:
        return render(request, 'services/profile.html',{'user': user})
      else:
       return render(request, 'home_user/index.html',{})


def edit_profile(request):
    user = get_user(request)
    if request.method =='POST':
        u_form = UserUpdateForm(request.POST ,request.FILES, instance=user)
        if u_form.is_valid():
            u_form.save()
            return redirect('services')
    else:
        u_form = UserUpdateForm(instance=user)
    context = {
        'u_form':u_form
            }
    return render(request,'services/user_update.html',context)

def sig(request):
    if 'user_id' in request.session:
     context = {
        'sig': Signaux.objects.filter(validate=True).order_by('-post_date')
     }
    return render(request,'services/signal.html',context)



