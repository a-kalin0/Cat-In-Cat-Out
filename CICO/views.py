from django.shortcuts import render
from django.views.generic import ListView
from .models import CiCoItem
from .models import Statuses
from django.shortcuts import redirect
from CICO.forms import ContactUsForm
from CICO.forms import ConnectionForm
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


def connection(request):

    if (request.method == "POST"):
        form = ConnectionForm(request.POST)
        if form.is_valid():
            #newItem = CiCoItem(text=form.cleaned_data["message"])
            #newItem.save()


            user = authenticate(username=form.cleaned_data["indentification"], password=form.cleaned_data["password"])
            if user is not None:

                # A backend authenticated the credentials
                return redirect(profileIndex)
                ...
            else:
                # No backend authenticated the credentials
                logger.info("login failed")




    else:
        form = ConnectionForm()
    return render(request, 'CICO/connexion.html', {"form": form})


def profileIndex(request):
    items = CiCoItem.objects.all()
    return render(request, 'CICO/profileIndex.html', {"items": items})


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