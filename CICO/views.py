from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import CiCoItem
from .models import Statuses
from .models import UserCICO
from .models import Cats
from .models import Cats
from CICO.forms import ContactUsForm
from CICO.forms import ConnectionForm
from CICO.forms import NewAccountForm
from CICO.forms import RequestNewPasswordForm
from CICO.forms import CatSubmitForm
import logging
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
logger = logging.getLogger('django')
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.files.storage import default_storage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CatSerializer
from django.core.exceptions import ValidationError





def Empty(request):
    return redirect("CICO/")

# Create your views here.

def checkIP(request):
    if request.session['IP'] != request.META.get("REMOTE_ADDR"):
        return False
    else:
        return True


class Void(ListView):
    model = CiCoItem
    template_name = "CICO/indexDefault.html"


def vue(request):
    return render(request, 'CICO/index.html')


def connection(request, formId):

    if (formId == 0):
        logout(request)
        request.session['IP'] = ""
        formId = 1

    if (formId == 1):
        if (request.method == "POST"):
            form = ConnectionForm(request.POST)
            if form.is_valid():
                #newItem = CiCoItem(text=form.cleaned_data["message"])
                #newItem.save()
                user = authenticate(username=form.cleaned_data["identification"], password=form.cleaned_data["password"])
                if user is not None:
                    login(request, user)
                    request.session['IP'] = request.META.get("REMOTE_ADDR")
                    request.session['user'] = user.id                # A backend authenticated the credentials
                    return redirect('profileIndex')
                else:
                    # No backend authenticated the credentials
                    logger.info("login failed")
        else:
            form = ConnectionForm()
    elif (formId == 2):
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
                    request.session['user'] = newUser.id  # A backend authenticated the credentials
                    return redirect('profileIndex')
        else:
            form = NewAccountForm()

    elif (formId == 3):
        ...
        if (request.method == "POST"):
            form = RequestNewPasswordForm(request.POST)
            if form.is_valid():
                emails = UserCICO.objects.values_list('email')
                if form.cleaned_data["email"] in emails:
                    #send mail
                    ...
        else:
            form = RequestNewPasswordForm()

    return render(request, 'CICO/connexion.html', {"form": form})


def profileIndex(request):
    if not checkIP(request):
        return render(request, 'CICO/unauthorized.html', status=401)
    items = CiCoItem.objects.all()
    print(request.user)
    print(request.META.get("REMOTE_ADDR"))
    user = request.user
    if request.user.is_authenticated:
        return render(request, 'CICO/profileIndex.html', {"items": items, "user": user.username})
    else:
        return render(request, 'CICO/unauthorized.html', status=401)



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

@login_required
def add_cat(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CatSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                cat = form.save(commit=False)
                cat.ownerId = request.user  # Set ownerId to the current user
                cat.clean()  # Call full_clean to run all other validations including clean()
                cat.save()
                return JsonResponse({'success': True, 'catName' : cat.name}, status=201)  # Or any other success response
            
            except ValidationError:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'errors': 'Invalid request'}, status=400)

class UserCatList(generics.ListAPIView):
    serializer_class = CatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cats.objects.filter(user=self.request.user)
    
@login_required
def get_cats(request):
    if request.user.is_authenticated:
        user_cats = Cats.objects.filter(ownerId_id=request.user).values_list('name', flat=True)
        return JsonResponse(list(user_cats), safe=False)
    return JsonResponse({'error': 'User not authenticated'}, status=401)
