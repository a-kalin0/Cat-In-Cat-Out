from django.shortcuts import render
from django.views.generic import ListView
from .models import CiCoItem
from .models import Statuses
from .models import UserCICO
from django.shortcuts import redirect
from CICO.forms import ContactUsForm
from CICO.forms import ConnectionForm
from CICO.forms import NewAccountForm
import logging
from django.contrib.auth import authenticate
logger = logging.getLogger('django')


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

    if (formId == 2):
        if (request.method == "POST"):
            form = NewAccountForm(request.POST)
            if form.is_valid():
                if form.cleaned_data["email"] in UserCICO.objects.values_list("email", flat = True):
                    logger.info("This email is already used") #these texts will need to be displayed on the page
                elif form.cleaned_data["password"] != form.cleaned_data["confirmPassword"]:
                    logger.info("Passwords not identical")
                elif form.cleaned_data["serial"] == False: #Insert here serial check function
                    logger.info("Wrong serial number")
                else:
                    # No backend authenticated the credentials
                    newUser = UserCICO.objects.create(email=form.cleaned_data["email"],
                                                      username=form.cleaned_data["identification"],
                                                      ownedDevice=form.cleaned_data["serial"])
                    newUser.set_password(form.cleaned_data["password"])
                    newUser.save()
                    request.session['user'] = newUser.id  # A backend authenticated the credentials
                    return redirect('profileIndex')
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
        return render(request, 'CICO/unauthorized.html')
    return render(request, 'CICO/profileIndex.html', {"items": items, "user":user})


def faq(request):
    return render(request, 'CICO/faq.html')


def contact(request):
    return render(request, 'CICO/contact.html')


def commande(request):
    return render(request, 'CICO/commande.html')


class PageMotE(ListView):
    model = CiCoItem
    template_name = "CICO/pageE.html"

    def get_queryset(self):
        return CiCoItem.objects.filter(text__icontains= "e")


class PageStatus(ListView):
    model = Statuses
    template_name = "CICO/pageStatus.html"
    ordering = ['heure']