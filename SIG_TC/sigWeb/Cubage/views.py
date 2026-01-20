from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.serializers import serialize

# Create your views here.
@login_required
def carte(request):
    liste_groupe=Groupemamora.objects.all()
    liste_serie=Serie.objects.all()
    liste_foret=Foret.objects.all()
    liste_canton=Canton.objects.all()
    liste_groupe_json = serialize('json', liste_groupe)
    liste_serie_json = serialize('json', liste_serie)
    liste_foret_json = serialize('json', liste_foret)
    liste_canton_json = serialize('json', liste_canton)
    
    context={
        'liste_groupe_json':liste_groupe_json,
        'liste_serie_json':liste_serie_json,
        'liste_foret_json':liste_foret_json,
        'liste_canton_json':liste_canton_json,



    }
    return render(request, "Cubage/carte.html", context)
 

def index(request):
    context={}
    return render(request, "Cubage/index.html", context)

def information(request):

    return render(request, "Cubage/informationGIS_tarif_cubage.html")

def info(request):

    return render(request, "Cubage/information_site_pas_connction.html")