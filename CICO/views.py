from django.shortcuts import render, redirect

from CICO.forms import ConnectionForm, NewAccountForm, ForgottenPassword, NewPassword, ContactUsForm, CatSubmitForm, CodeForm, AddDeviceNumber
from django.contrib.auth import authenticate, login, get_user_model, logout
from .models import UserCICO, Cats, DeviceRecords, CatsAdventures, Trigger
from django.views.generic import ListView
import logging
logger = logging.getLogger('django')
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, password_reset_token
from django.db.models import F
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
import os
from random import randint
from datetime import datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.core.files.storage import default_storage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CatSerializer
from django.dispatch import receiver
from django.db.models.signals import post_delete

LIST_SIZE = 5

@receiver(post_delete, sender=Trigger)
def deleting_model(sender, instance, **kwargs):

    DeviceRecords.objects.get(recordId=instance.recordId_id).delete()
    print("a")
    print(instance.recordId_id)

@csrf_exempt
def postRaspberry(request):
    if request.method == 'POST':
        # print(request.FILES)
        # print(request.POST)
        for key, uploaded_file in request.FILES.items():
            owner = UserCICO.objects.get(ownedDevice=request.POST["deviceId"])
            cat = None
            isCat = True
            if isCat:
                cat = Cats.objects.filter(ownerId=owner)[2]
            # print(cat)
            fileName = str(uploaded_file)
            AddRecord(owner, fileName.split("-")[0].upper(), isCat, uploaded_file, cat)

        return JsonResponse({"message": "Photos enregistrées avec succès"})
    else:
        return JsonResponse({"error": "Aucune photo reçue"}, status=400)



def UpdateList(request, deviceId, date="00-00-000"):
    recordList = GetRecords(deviceId, date)[::-1]
    newList = recordList[request.session['listStart']:request.session['listStart'] + LIST_SIZE]
    if len(newList) == 0:
        newList = recordList[request.session['listStart'] - LIST_SIZE:request.session['listStart']]
        request.session['listStart'] -= LIST_SIZE

    return newList

def GetRecords(deviceId,date):
    if date == "00-00-0000":
        querySet = DeviceRecords.objects.filter(deviceId=deviceId).annotate(catName=F('trigger__catId__name'))
    else:
        dateObject = datetime.strptime(date, '%Y-%m-%d').date()
        querySet = DeviceRecords.objects.filter(deviceId=deviceId,
            time__year=dateObject.year, time__month=dateObject.month,
                                            time__day=dateObject.day).annotate(catName=F('trigger__catId__name'))
    return querySet.values()



def AddRecord(deviceOwner,event,isCat, photo, cat = None):
    newRecord = DeviceRecords.objects.create(deviceId=deviceOwner,event=event,isCat=isCat, image=photo)
    if isCat:
        newTrigger = Trigger.objects.create(catId=cat, recordId=newRecord)

def Empty(request):
    return redirect("CICO/")


def checkIP(request):
    print(request.session['IP'], request.META.get("REMOTE_ADDR"))
    if request.session['IP'] != request.META.get("REMOTE_ADDR"):
        return False
    else:
        return True


def vue(request):
    return render(request, 'CICO/index.html')

def generateCode():
    return str(randint(100000,999999)) #starts from 100000 to be sure that the number has at least 6 digits (and i'm too lazy to find a better way to do it)

def mail_sent(request):
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["code"] == request.session["validationCode"]:
                request.session["validationCode"] = ""

                if request.session["validating"] == "newAccount":
                    user = UserCICO.objects.get(email=request.session["passwordResetEmail"])
                    user.is_active = True
                    user.save()
                    login(request, user)
                    request.session['IP'] = request.META.get("REMOTE_ADDR")
                    request.session['user'] = user.id
                    return redirect('profileIndex')
                elif request.session["validating"] == "newPassword":
                    return redirect(newpassword)
            else:
                print("wrong code")
        else:
            print("form invalid")
    form = CodeForm()
    return render(request, 'CICO/mail_sent.html', {"form":form})


def reset_done(request):
     return render(request, "CICO/password_reset_complete.html")


def logoutPage(request):
    logout(request)
    request.session['IP'] = ""
    return redirect("connexion", formType="connexion")


def connection(request, formType):
    message = ""

    if (formType == "connexion"):
        if (request.method == "POST"):
            form = ConnectionForm(request.POST)
            if form.is_valid():
                user = authenticate(username=form.cleaned_data["identification"],
                                    password=form.cleaned_data["password"])
                if user is not None:
                    login(request, user)
                    request.session['IP'] = request.META.get("REMOTE_ADDR")
                    request.session['user'] = user.id
                    return redirect('profileIndex')
                else:
                    message = "Mauvais mot de passe ou identifiant"
                    logger.info("login failed")
        else:
            form = ConnectionForm()
    elif (formType == "nouveauCompte"):
        if (request.method == "POST"):
            form = NewAccountForm(request.POST)
            if form.is_valid():
                if form.data["newAccount-identification"] in UserCICO.objects.values_list("username", flat=True):
                    logger.info("This username is already used")
                    message = "This username is already used"
                elif form.data["newAccount-email"] in UserCICO.objects.values_list("email", flat=True):
                    logger.info("This email is already used")  # these texts will need to be displayed on the page
                    message = "This email is already used"
                elif form.data["newAccount-password"] != form.data["newAccount-confirmPassword"]:
                    logger.info("Passwords not identical")
                    message = "Passwords not identical"
                else:
                    newUser = UserCICO.objects.create(email=form.cleaned_data["email"],
                                                      username=form.cleaned_data["identification"])
                    newUser.set_password(form.cleaned_data["password"])
                    newUser.is_active = False
                    newUser.save()
    
                    current_site = get_current_site(request) #osef?

                    request.session["validating"] = "newAccount"
                    request.session["passwordResetEmail"] = newUser.email
                    request.session["validationCode"] = generateCode()

                    subject = "Confirmation d'inscription"
                    email_template_name = "CICO/acc_activate_email.html"
                    c = {
                        "email": newUser.email,
                        'site_name': 'YourWebsite',
                        "user": newUser,
                        "code": request.session["validationCode"],
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'server@example.com', [newUser.email], fail_silently=False)
                    except Exception as e:
                        return HttpResponse('Invalid header found.')

                    return redirect('../mail_sent')

                    #request.session['user'] = newUser.id  # A backend authenticated the credentials
                    #return redirect('profileIndex')


        else:
            form = NewAccountForm()

    return render(request, 'CICO/connexion.html', {"form": form, "message": message})

def profileIndex(request):
    if not checkIP(request) or not request.user.is_authenticated:
        return render(request, 'CICO/unauthorized.html', status=401)
    if (UserCICO.objects.get(username=request.user).ownedDevice == None):
        return redirect("profileNoDevice")
    try:
        request.session['listStart']
    except:
        request.session['listStart'] = 0

    try:
        request.session["filterDate"]
    except:
        request.session["filterDate"] = "00-00-0000"



    if request.method == "GET":
        user_cats = Cats.objects.filter(ownerId=request.user)

        end_date = timezone.now()

        start_date = end_date - timedelta(days=6)

        triggers = Trigger.objects.filter(
            catId__in=user_cats,
            recordId__time__range=[start_date, end_date]
        )

        xValues = [day.strftime("%A") for day in (start_date + timedelta(n) for n in range(7))]

        barColors = ["red", "green", "blue", "orange", "brown"]

        cat_data = {cat.name: {'entrees': [0]*7, 'sorties': [0]*7} for cat in user_cats}

        for trigger in triggers:
            record = trigger.recordId
            day_of_week = record.time.strftime("%A")
            cat_name = trigger.catId.name
            index_day = xValues.index(day_of_week)

            if record.event == "IN":
                cat_data[cat_name]['entrees'][index_day] += 1
            elif record.event == "OUT":
                cat_data[cat_name]['sorties'][index_day] += 1
        
        recordList = UpdateList(request, UserCICO.objects.get(username=request.user).ownedDevice, request.session["filterDate"] )
        context = {
            "user": request.user.username,
            "recordList": recordList, 
            "xValues": xValues,
            "cat_data": cat_data,
            "barColors": barColors,
            "date":request.session["filterDate"],
        }

        return render(request, 'CICO/profileIndex.html', context)
    
    elif request.method == "POST":
        try:
            datetime.strptime(request.POST["bouton"], '%Y-%m-%d').date()
        except:
            print("no date selected, using default value")
        else:
            request.session["filterDate"] = request.POST["bouton"]
            request.session['listStart'] = 0

        if request.POST["bouton"] == "Annuler":
            request.session["filterDate"] = "00-00-0000"
        elif request.POST["bouton"] == "récent":
            request.session['listStart'] = max(0, request.session[
            'listStart'] - LIST_SIZE)  # the max function is used to prevent the substraction from resulting in a negative
        elif request.POST["bouton"] == "ancien":
            request.session['listStart'] += LIST_SIZE

    
    return redirect("profileIndex")



def getProfileIndex(request, recordList):
    return render(request, 'CICO/profileIndex.html')

def profileNoDevice(request):
    message = ""
    if (request.method == "POST"):
        form = AddDeviceNumber(request.POST)
        if form.is_valid():
            number = form.cleaned_data["deviceNumber"]
            if number in UserCICO.objects.values_list("ownedDevice", flat=True):
                message = "Wrong device number"
                return render(request, 'CICO/profileNoDevice.html', {"form": form, "message": message})
            user = UserCICO.objects.get(username=request.user)
            user.ownedDevice = number
            user.save()
            return redirect('profileIndex')
    else:
        form = AddDeviceNumber()
        return render(request, 'CICO/profileNoDevice.html', {"form":form})


def faq(request):
    return render(request, 'CICO/faq.html')


def contact(request):
    return render(request, 'CICO/contact.html')


def commande(request):
    return render(request, 'CICO/commande.html')
    


def activate(request, uidb64, token):
    """Check the activation token sent via mail"""
    User = get_user_model()
    print(request.POST["uidb64"])
    print(request.POST["token"])
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
    

def forgotpassword(request):
    if request.method == "POST":
        password_reset_form = ForgottenPassword(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            request.session["validating"] = "newPassword"
            request.session["passwordResetEmail"] = data
            request.session["validationCode"] = generateCode()
            associated_users = UserCICO.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "CICO/password_reset_email.html"
                    c = {
                        "email": user.email,
                        'site_name': 'YourWebsite',
                        "user": user,
                        "code": request.session["validationCode"],
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'server@example.com', [user.email], fail_silently=False)
                    except Exception as e:
                        return HttpResponse('Invalid header found.')
                return redirect('mail_sent')
    password_reset_form = ForgottenPassword()
    return render(request, "CICO/resetpassword.html", context={"password_reset_form": password_reset_form})


def newpassword(request):
    if request.method == 'POST':
        new_password_form = NewPassword(request.POST)
        if new_password_form.is_valid():
            new_password = new_password_form.cleaned_data['newPassword']
            user = UserCICO.objects.get(email=request.session["passwordResetEmail"])
            user.set_password(new_password)
            user.save()
            request.session["passwordResetEmail"] = ""
            logger.info(f"Password changed for user {user.username}")
            return redirect('reset_done')  # Rediriger vers la page de réussite
    else:
        new_password_form = NewPassword()

    return render(request, "CICO/newpassword.html", context={"form": new_password_form})


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
                catsAndStatus = [cat.name, cat.catId,
                                      cat.getStatus()["status"]]


                return JsonResponse({'success': True, 'catsAndStatus': catsAndStatus}, status=201)  # Or any other success response
            
            except ValidationError:
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'errors': 'Invalid request'}, status=400)
    
@login_required
def get_cats(request):
    if request.user.is_authenticated:
        user_cats = Cats.objects.filter(ownerId_id=request.user).values_list('name', 'catId')
        catsAndStatus = []
        for i in range(len(user_cats)):
            catsAndStatus.append([user_cats[i][0], user_cats[i][1], Cats.objects.filter(ownerId_id=request.user)[i].getStatus()["status"]])
        return JsonResponse(catsAndStatus, safe=False)
    return JsonResponse({'error': 'User not authenticated'}, status=401)


@login_required
def get_cat_details(request, catId):
    # Fetch the cat details
    cat = Cats.objects.get(ownerId_id=request.user, catId=catId)
    return JsonResponse({
        'name': cat.name,
        'image_url': cat.image.url if cat.image else ''
    })


@login_required
def delete_cat(request, catId):
    cat = get_object_or_404(Cats, catId=catId, ownerId_id=request.user)
    if cat.image:
        if os.path.isfile(cat.image.path):
            os.remove(cat.image.path)
    cat.delete()
    return JsonResponse({'message': 'Cat deleted successfully'})

@login_required
def modify_cat(request, catId):
    cat = get_object_or_404(Cats, catId=catId, ownerId_id=request.user)
    if request.method == 'POST':
        form = CatSubmitForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True, 
                'message': 'Cat modified successfully',
                'catId': str(cat.catId),  # Assuming catId is a UUID
                'newName': cat.name
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})
  
def profile(request):
    if not checkIP(request) or not request.user.is_authenticated:
        return render(request, 'CICO/unauthorized.html', status=401)

    user = UserCICO.objects.get(username=request.user)

    if request.method == "POST":
        if list(request.POST.keys())[1] == "deleteAccount":
            user.delete()
            return redirect("connexion", formType="connexion")
        setattr(user,str(list(request.POST.keys())[1]), str(list(request.POST.values())[1]))
        user.save()
        return redirect("profile")
    else:
        return render(request, "CICO/profile.html", {"user":user})
