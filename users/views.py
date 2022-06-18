import threading
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Users, Service
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.core.mail import EmailMessage
from .utils import generate_token
from django.conf import settings
from rest_framework import viewsets

from .models import Service , Role , Users

from rest_framework import generics
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


from django.contrib.auth import logout as auth_logout


# Create your views here.





def get_user(request):
    return Users.objects.get(id=request.session['user_id'])

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

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


def signin_signup(request):
    if request.method == "POST":
        context = {'has_error': False}
        btn1 = request.POST.get("signup")
        btn2 = request.POST.get("signin")
        Username = request.POST.get("username")
        Name = request.POST.get("name")
        Surname = request.POST.get("surname")
        Email = request.POST.get("email")
        Password1 = request.POST.get("password1")
        Password2 = request.POST.get("password2")
        Username1 = request.POST.get("username1")
        Password = request.POST.get("password")

        if btn1:
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
                return render(request, 'users/login.html')
            else:
                return render(request, 'users/login.html')
        if btn2:
            try:

                user = Users.objects.get(username=Username1)

                checkpassword = check_password(Password, user.password)
                if checkpassword:

                    if not user.is_active:
                        messages.add_message(request, messages.ERROR, "votre compte est désactivé")
                        return render(request, "users/login.html")

                    request.session['user_id'] = user.pk
                    request.session['username'] = user.username
                    if 'user_id' in request.session:
                        user = get_user(request)

                        if user.role.name == "utilisateur" or user.role.name == "admin":
                            return redirect(reverse('categorie'))

                        if user.role.name == "responsable":
                            return redirect(reverse('manage'))

                        if user.role.name.__contains__('service'):
                            return redirect('services')
                        if user.role.name == "administration" or user.role.name == "club":
                            return redirect(reverse('administration'))
                if not checkpassword:
                    messages.add_message(request, messages.ERROR, "password incorrect")





            except Users.DoesNotExist as e:
                messages.add_message(request, messages.ERROR, "username invalide")
                return render(request, "users/login.html")

    return render(request, 'users/login.html')


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
        return redirect(reverse('signin&signup'))

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
            messages.error(request, "Entrer un valide email")
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
            return redirect('signin&signup')
        except Exception as e:
            messages.info(request, "opss,quelque chose s'est mal passé !")
            return render(request, 'users/set-new-password.html', context)

@login_required
def profile(request):
    if 'user_id' in request.session:
        user = get_user(request).pk
        data = Users.objects.get(pk=user)
        context = {
            'data': data
        }

    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if 'user_id' in request.session:
        user = get_user(request).pk
        data = Users.objects.get(pk=user)
        context = {
            'data': data
        }

        if request.method == "POST":

            Username = request.POST.get("username")
            Name = request.POST.get("name")
            Surname = request.POST.get("surname")
            Email = request.POST.get("email")
            Password1 = request.POST.get("password1")
            Password2 = request.POST.get("password2")
            if not Users.objects.filter(username=Username).exists():
                data.username = Username

            data.first_name = Name
            data.last_name = Surname

            if len(request.FILES) != 0:
                data.image = request.FILES['image']
            if len(Password1) >= 8 and Password2 == Password1:
                data.password = Password1
                data.set_password(data.password)


            if not Users.objects.filter(email=Email).exists():
                data.email = Email
                data.is_active = False
                data.save()
                send_activation_email(data, request)
                messages.add_message(request, messages.SUCCESS, "nous avons vous envoyer un email")
                return redirect('signin&signup')

            data.save()
            messages.add_message(request, messages.SUCCESS, "modification est sauvgardé")
            return redirect('profile')

    return render(request, 'users/edit_profile.html', context)


def logout(request):
    try:

        del request.session['user_id']
        messages.add_message(request,messages.INFO,"vous avez déconnecté")

    except KeyError:
        pass
    return redirect('signin&signup')
