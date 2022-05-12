import threading
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Users,Service
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import EmailMessage
from .utils import generate_token
from django.conf import settings







# Create your views here.

def get_user(request):
    return Users.objects.get(id=request.session['user_id'])



# for user to not wait
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('users/activate.html', {
        'user': user.username,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)

    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_HOST_USER,
                         to=[user.email]
                         )
    EmailThread(email).start()


def signup(request):
    if request.method == "POST":
        context = {'has_error': False}
        Username = request.POST.get("username")
        Name = request.POST.get("name")
        Surname = request.POST.get("surname")
        Email = request.POST.get("email")
        Password1 = request.POST.get("password1")
        Password2 = request.POST.get("password2")

        if Password1 != Password2:
            messages.add_message(request, messages.ERROR, "vérifier votre mot de passe")
            context['has_error'] = True
        if not Username:
            context['has_error'] = True
        if not Name:
            context['has_error'] = True
        if not Surname:
            context['has_error'] = True

        if Users.objects.filter(username=Username).exists():
            messages.add_message(request, messages.ERROR, "username est déjà utiliser")
            context['has_error'] = True

        if Users.objects.filter(email=Email).exists():
            messages.error(request, "email est déjà utiliser")
            context['has_error'] = True

        if not context['has_error']:

            user = Users(username=Username, first_name=Name, last_name=Surname, email=Email, password=Password1)
            user.set_password(user.password)
            user.is_active = False
            user.save()

            # send verification email
            send_activation_email(user, request)

            messages.add_message(request, messages.SUCCESS, "nous avons vous envoyer un email")
            return render(request, 'users/signup.html')
        else:
            return render(request, 'users/signup.html')

    else:
        return render(request, 'users/signup.html')


def signin(request):
    if request.method == "POST":
        try:

            Username = request.POST.get("username")
            Password = request.POST.get("password")

            user = Users.objects.get(username=Username)

            checkpassword = check_password(Password, user.password)
            if checkpassword:



                if not user.is_active:
                    messages.add_message(request, messages.ERROR, "votre compte est désactivé")
                    return render(request, "users/login.html")

                request.session['user_id'] = user.pk
                request.session['username'] = user.username
                if 'user_id' in request.session:
                    user=get_user(request)
                    messages.add_message(request, messages.SUCCESS, "vous avez sidentifier")
                    if user.role=="utilisateur":
                        return redirect(reverse('categorie'))
                    if user.role=="responsable":
                        return redirect(reverse('manage'))
                    service = user.role
                    if Service.objects.filter(name=service):
                        return HttpResponse("Hello")
                    if user.role=="administration" or user.role=="club":
                        return redirect(reverse('add_announcement'))




        except Users.DoesNotExist as e:
            messages.add_message(request, messages.ERROR, "username et password sont invalides")
            return render(request, "users/login.html")

    return render(request, "users/login.html")




def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Users.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, " email verifier sidentifier maintenant")
        return redirect(reverse('signin'))

    return render(request, "users/activate_failed.html")


# Reset Password
class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'users/reset_password.html')

    def post(self, request):
        Email = request.POST.get('email')
        current_site = get_current_site(request)
        user = Users.objects.filter(email=Email)
        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': generate_token.make_token(user[0])

            }

            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']

            })

            email_subject = 'Reset your password'
            reset_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                email_subject,
                "Hi there, please click the link below to reset your password \n" + reset_url,
                'madrasaticesi@gmail.com',
                [Email],
            )

            EmailThread(email).start()
            messages.success(request, "nous avons vous envoyer un email")
        else:
            messages.error(request,"Entrer un valide email")
        return render(request, 'users/reset_password.html')


class CompleteResetPassword(View):
    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }


        return render(request, 'users/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        Password1 = request.POST.get("password1")
        Password2 = request.POST.get("password2")

        if Password1 != Password2:
            messages.add_message(request, messages.ERROR, "vérifier votre mot de passe")
            return render(request, 'users/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = Users.objects.get(pk=user_id)
            user.password = Password1
            user.set_password(user.password)
            user.save()
            messages.add_message(request, messages.SUCCESS, "Mot de passe réinitialisé avec succès!")
            return redirect('signin')
        except Exception as e:
            messages.info(request, "opss,quelque chose s'est mal passé !")
            return render(request, 'users/set-new-password.html', context)

