from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import CiCoItem, Statuses, UserCICO
from CICO.forms import ConnectionForm, NewAccountForm, ForgottenPassword, NewPassword
import logging
from django.contrib.auth import authenticate, login, get_user_model
logger = logging.getLogger('django')
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token


def Empty(request):
    return redirect("CICO/")

# Create your views here.


class Void(ListView):
    model = CiCoItem
    template_name = "CICO/indexDefault.html"


def vue(request):
    return render(request, 'CICO/index.html')


def connection(request, formId):
    request.session["user"] = None

    if (formId == 2): #inscription
        if (request.method == "POST"):
            form = NewAccountForm(request.POST)
            if form.is_valid():
                if form.cleaned_data["email"] in UserCICO.objects.values_list("email", flat = True):
                    logger.info("This email is already used") #these texts will need to be displayed on the page
                elif form.cleaned_data["password"] != form.cleaned_data["confirmPassword"]:
                    logger.info("Passwords not identical")
                else:
                    # No backend authenticated the credentials
                    newUser = UserCICO.objects.create(email=form.cleaned_data["email"],
                                                      username=form.cleaned_data["identification"])
                    newUser.set_password(form.cleaned_data["password"])
                    newUser.save()
                    current_site = get_current_site(request)
                    mail_subject = "Confirmation d'inscription"
                    message = render_to_string('CICO/acc_activate_email.html', {
                                'user': newUser,
                                'domain': current_site.domain,
                                'uid':urlsafe_base64_encode(force_bytes(newUser.pk)),
                                'token':account_activation_token.make_token(newUser),
                            })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return HttpResponse('Please confirm your email address to complete the registration')

                    #request.session['user'] = newUser.id  # A backend authenticated the credentials
                    #return redirect('profileIndex')
        else:
            form = NewAccountForm()
    else:
        if (request.method == "POST"):
            form = ConnectionForm(request.POST)
            if form.is_valid():
                #newItem = CiCoItem(text=form.cleaned_data["message"])
                #newItem.save()
                user = authenticate(username=form.cleaned_data["identification"], password=form.cleaned_data["password"])
                if user is not None:
                    request.session['user'] = user.id                # A backend authenticated the credentials
                    return redirect('profileIndex')
                else:
                    # No backend authenticated the credentials
                    logger.info("login failed")
        else:
            form = ConnectionForm()
    return render(request, 'CICO/connexion.html', {"form": form})


def profileIndex(request):
    items = CiCoItem.objects.all()
    print(request.session['user'])
    user = None
    try:
        user = UserCICO.objects.get(id=request.session['user'])
    except (KeyError, UserCICO.DoesNotExist):
        user = None
    print(user)
    if (user==None):
        return render(request, 'CICO/unauthorized.html', status=401)
    return render(request, 'CICO/profileIndex.html', {"items": items, "user":user})


def faq(request):
    return render(request, 'CICO/faq.html')


def contact(request):
    return render(request, 'CICO/contact.html')


def commande(request):
    return render(request, 'CICO/commande.html')

def forgottenpassword(request):
    form = ForgottenPassword()
    return render(request, 'CICO/resetpassword.html', {"form": form})


class PageMotE(ListView):
    model = CiCoItem
    template_name = "CICO/pageE.html"

    def get_queryset(self):
        return CiCoItem.objects.filter(text__icontains= "e")


class PageStatus(ListView):
    model = Statuses
    template_name = "CICO/pageStatus.html"
    ordering = ['heure']


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/CICO')
    else:
        return HttpResponse('Activation link is invalid!')
    

def resetpassword():
# faut que le formulaire soit valide ==> adresse mail dans la db 
# si il n'est pas valide ==> message en rouge (Votre adresse mail n'est pas valide)
# si il est valide ==> Message en vert (Un mail de réinitialisation vous a été envoyé)
# envoi de mail => tu gères ça normalement
# cliquage sur lien = formulaire avec nouveau mot de passe + confirmation de mot de passe
# si okay alors remplacer le mdp dans la db ==> faire gaffe aux potentielles attaques par injection
# si pas okay ==> message en rouge 
# retour à la page d'accueil
    return ("hello world")