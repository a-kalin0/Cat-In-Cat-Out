from django.shortcuts import render
from django.views.generic import ListView
from .models import CiCoItem
from .models import TableStatus
from django.shortcuts import redirect


def Empty(request):
    return redirect("CICO/")

# Create your views here.

class Void(ListView):
    model = CiCoItem
    template_name = "CICO/indexDefault.html"


def vue(request):
    items = CiCoItem.objects.all()
    return render(request, 'CICO/index.html', {"items": items})


class PageMotE(ListView):
    model = CiCoItem
    template_name = "CICO/pageE.html"

    def get_queryset(self):
        return CiCoItem.objects.filter(text__icontains= "e")


class PageStatus(ListView):
    model = TableStatus
    template_name = "CICO/pageStatus.html"
    ordering = ['heure']