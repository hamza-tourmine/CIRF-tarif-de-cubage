from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, get_object_or_404
from .models import *
from .forms import *
from decimal import Decimal
import numpy as np
from scipy import stats
import math 
from django.core.exceptions import ObjectDoesNotExist


#____________________________________________________________________________________________________________________________________

# vue pour chercher le tarif de cubage et pour la creation l'objet operation et des strates
@login_required 
def index(request):
    if request.method == 'POST':
        form = TarifCubageForm(request.POST)
        if form.is_valid():
            foret = form.cleaned_data['foret']
            canton = form.cleaned_data['canton']
            essence = form.cleaned_data['essence']
            regime = form.cleaned_data['regime']
            try:
                foret_objets = Foret.objects.get(nom=foret)
                canton_object = Canton.objects.get(nom=canton, foret=foret_objets)
                regime_objet = Regime.objects.get(Nom=regime)
                essence_object=Essences.objects.get(Nom=essence, canton=canton_object, Regime=regime_objet)
                essence_id=essence_object.id
                return redirect('Cubageindividuel:choixtarifCubage', essence_id)
            except ObjectDoesNotExist as e:
                messageError="L'essence qui possède ces critères de recherche n'existe pas dans la base de données"
                context = {
                    'form': form,
                    'message': messageError,
                    
                    
                    }
                return render(request, "Cubageindividuel/index.html", context)



    else:
         form = TarifCubageForm()

    context = {'form': form}
    return render(request, "Cubageindividuel/index.html", context)

#__________________________________________________________________________________________________________________________________________________________

def choixTarif_cubage_formulaire(request, essence_id):
    essence_object = Essences.objects.get(id=essence_id)
    context={}

    if request.method == 'POST':
        form = choixTarifCubageForm(request.POST, essence=essence_object)
        if form.is_valid():
            tarif_cubage_selectionner = form.cleaned_data['tarif_de_cubage']
            Nom_projet=form.cleaned_data['Nom_projet']
            tarifCubage=TarifCubage.objects.get(id=tarif_cubage_selectionner)
            typeEchantillonage=TypeEchantillonage.objects.get(id=4)
            operation_objet=Operation_de_calcul.objects.create(TarifCubage=tarifCubage, TypeEchantillonage=typeEchantillonage, Nom=Nom_projet)
            strate = Strate.objects.create(Operation_de_calcul=operation_objet)
            strate_id=strate.id
            placette = Placette.objects.create(Strate=strate)
            placette_id=placette.id
            formule_tarif=tarifCubage.formule
            circonf_min=tarifCubage.circonference_min
            circonf_max=tarifCubage.circonference_max 

            Lettre='h'
            def calculer_volume(formule, circonference):
                formule_avec_virgule=formule
                formule_avec_point=formule_avec_virgule.replace(',', '.')
                C=circonference
                volume= eval(formule_avec_point)
                return volume/1000
            if Lettre in formule_tarif.lower():
                for circonf in range(circonf_min, circonf_max + 1, 10):
                    bois=liste_de_bois.objects.create(Placette=placette,  circonferance_1m30=circonf, 
                                                    volume_individuel=0, nombre_de_bois_classe=0,
                                                    volume_total_classe=0, hauteur=0 )
            else:
                #calcul de volume selon la circonference
                for circonf in range(circonf_min, circonf_max + 1, 10):
                    volume_par_classe = calculer_volume(formule_tarif, circonf)
                    bois=liste_de_bois.objects.create(Placette=placette,  circonferance_1m30=circonf, 
                                                    volume_individuel=volume_par_classe, nombre_de_bois_classe=0,
                                                    volume_total_classe=0, hauteur=0 )



            
            context={
                'placette_id': placette_id, 
                'strate_id':strate_id,
                'strate': strate
            }

            return render(request,'Cubageindividuel/informations_calcul.html', context)

    else:
        form = choixTarifCubageForm(essence=essence_object)

    context = {
        'form': form,
    }

    return render(request, 'Cubageindividuel/choix_tarif.html', context)

#____________________________________________________________________________________________________________________________________________________

def calculVolume_bois(request, placette_id):
    placette = Placette.objects.get(pk=placette_id)
    liste_de_bois_par_placette=liste_de_bois.objects.filter(Placette=placette).order_by('circonferance_1m30')
    labels=[]
    Nombrebois=[]
    volumebois=[]
    
    for bois in liste_de_bois_par_placette:
        labels.append(bois.circonferance_1m30)
        Nombrebois.append(bois.nombre_de_bois_classe)
        volumetot=int(bois.volume_total_classe)
        volumebois.append(volumetot)
        

    formule=placette.Strate.Operation_de_calcul.TarifCubage.formule
    Lettre='h'
    presence_hauteur=None
    if Lettre in formule.lower():
        presence_hauteur=True
    else:
        presence_hauteur=False
    context={
        "liste_de_bois_par_placette": liste_de_bois_par_placette,
        "placette_id":placette_id,
        'presence_hauteur': presence_hauteur,
        'labels': labels,
        'Nombrebois': Nombrebois,
        'volumebois': volumebois, 
    }
    return render(request, "Cubageindividuel/liste_de_bois.html", context)


#____________________________________________________________________________________________________________________________________________________

def formulaire_liste_bois(request, placette_id):
    placette = Placette.objects.get(pk=placette_id)
    formule_Tarifs=placette.Strate.Operation_de_calcul.TarifCubage.formule
    Lettre='h'
    if Lettre in formule_Tarifs.lower():
        if request.method == 'POST':
            for bois_id, nombre_bois, hauteur_bois in zip( request.POST.getlist('bois_id'), request.POST.getlist('nombre_bois'),request.POST.getlist('hauteur_bois') ):
                bois = liste_de_bois.objects.get(id=bois_id)
                bois.nombre_de_bois_classe= Decimal(nombre_bois)
                bois.hauteur=Decimal(hauteur_bois)
                circonference_1m30=bois.circonferance_1m30

                def calculer_volume(formule, circonference, hauteur):
                    formule_avec_virgule=formule
                    formule_avec_point=formule_avec_virgule.replace(',', '.')
                    C=float(circonference)
                    H=float(hauteur)
                    volume= eval(formule_avec_point)
                    return volume/1000


                volumeindi= calculer_volume(formule_Tarifs, circonference_1m30, hauteur_bois)
                bois.volume_individuel=volumeindi
                bois.volume_total_classe = Decimal(nombre_bois)*Decimal(volumeindi)
                bois.save()
            return redirect('Cubageindividuel:Calcule', placette_id) 
    else:
        if request.method == 'POST':
            for bois_id, nombre_bois in zip( request.POST.getlist('bois_id'), request.POST.getlist('nombre_bois')):
                bois = liste_de_bois.objects.get(id=bois_id)
                bois.nombre_de_bois_classe= Decimal(nombre_bois)
            
                volumeindi= bois.volume_individuel
                bois.volume_total_classe = Decimal(nombre_bois)*volumeindi
                bois.save()
            return redirect('Cubageindividuel:Calcule', placette_id)

    placette = Placette.objects.get(pk=placette_id)
    
    liste_de_bois_par_placette=liste_de_bois.objects.filter(Placette=placette).order_by('circonferance_1m30')
   

    context={
        "liste_de_bois_par_placette": liste_de_bois_par_placette,
        "placette_id":placette_id,
        
    }
    return render(request, 'Cubageindividuel/liste_de_bois.html', context)

#___________________________________________________________________________________________________________________________________________________________

def Calcul_somme_total_bois(request, placette_id):
    placette = Placette.objects.get(pk=placette_id)
    
    
    liste_de_bois_par_placette=liste_de_bois.objects.filter(Placette=placette)
    liste_volume_total_par_circonference=[]
    liste_nombre_bois_par_circonference=[]
    for bois in liste_de_bois_par_placette:
        liste_volume_total_par_circonference.append(bois.volume_total_classe)
        liste_nombre_bois_par_circonference.append(bois.nombre_de_bois_classe)
         
    #volume total d
    if placette:
        volume_total_par_placette=sum(liste_volume_total_par_circonference)
        placette.volume_total=volume_total_par_placette
        nombre_bois_total=sum(liste_nombre_bois_par_circonference)
        placette.nombre_de_bois_total=nombre_bois_total
        placette.save()

        #recuperation des données 
        Strate=placette.Strate
        operation_de_calcul=Strate.Operation_de_calcul
        TarifCubage=operation_de_calcul.TarifCubage
        tarif_cubage_utilise = TarifCubage.formule
        intervalle_de_validite=[TarifCubage.circonference_min, TarifCubage.circonference_max]
        

        #information 
        essence_objet=TarifCubage.Essence
        essencename=essence_objet.Nom
        Canton_object=essence_objet.canton
        canton_name=Canton_object.nom
        Foret=Canton_object.foret.nom
        regime=TarifCubage.Essence.Regime.Nom

        context={
            'placette': placette, 
            'essence': essencename,
            'canton_name':canton_name,
            'Foret':Foret,
            'regime':regime,
            'FormuleTarif': tarif_cubage_utilise,
            'intervalle_validite': intervalle_de_validite,
            'Strate':Strate,
            'nombre_bois_total':nombre_bois_total,
            'liste_de_bois':liste_de_bois_par_placette
        }

    
        return render(request, 'Cubageindividuel/resulat.html', context)
    else:
        raise('il ya une erreur')

           
#_______________________________________________________________________________________________________________________________

def strateformulaire(request, strate_id):
    #recuperation de l'objet strate pour le remplissage automatique du formulaire
    strate_objet = get_object_or_404(Strate, id=strate_id)
    #recuperation de l'objet operation pour le redirect vers les strates 
    placette = Placette.objects.get(Strate=strate_objet)
    placette_id=placette.id
    context={}

    if request.method == 'POST':
        form = StratesForm(request.POST, instance=strate_objet)
        if form.is_valid():
            form.save()
            context={
                'placette_id': placette_id, 
                'strate_id':strate_id, 
                'strate': strate_objet
            }

            return render(request,'Cubageindividuel/informations_calcul.html', context)     

    else:
        form = StratesForm(instance=strate_objet)

    context = {
        'form': form,
        'strate': strate_objet,
        
    }
    return render(request, "Cubageindividuel/strates_detail.html", context)     

#________________________________________________________________________________________________________________
@login_required
def operation_list_individuel(request):
    operations_liste = Operation_de_calcul.objects.filter(TypeEchantillonage__id='4')

    return render(request, 'Cubageindividuel/operation_list.html', {'operations_liste': operations_liste})



def operation_delete(request, pk):
    operation = get_object_or_404(Operation_de_calcul, pk=pk)
    if request.method == 'POST':
        operation.delete()
        return redirect('Cubageindividuel:operation_list_individuel')
    return render(request, 'Cubageindividuel/operation_confirm_delete.html', {'operation': operation})


def Consulter_info(request, pk):
    operations_object = Operation_de_calcul.objects.get(id=pk)
    strate=Strate.objects.get(Operation_de_calcul=operations_object)
    strate_id=strate.id
    placette=Placette.objects.get(Strate=strate)
    placette_id=placette.id

    context={
                'placette_id': placette_id, 
                'strate_id':strate_id,
                'strate': strate
            }

    return render(request,'Cubageindividuel/informations_calcul.html', context)