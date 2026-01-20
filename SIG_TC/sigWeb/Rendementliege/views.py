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
    context={}
    if request.method == 'POST':
        form = TarifCubageForm(request.POST)
        if form.is_valid():
            foret = form.cleaned_data['foret']
            canton = form.cleaned_data['canton']
            essence = form.cleaned_data['essence']
            regime = form.cleaned_data['regime']

            # Récupération des objets associés aux choix du formulaire
            try:
                foret_objets = Foret.objects.get(nom=foret)
                canton_object = Canton.objects.get(nom=canton, foret=foret_objets)
                regime_objet = Regime.objects.get(Nom=regime)

                essence_object_liege_femelle=Essenceliège.objects.get(Nom=essence, canton=canton_object, Regime=regime_objet, Typeliège='Liège de reproduction')
                tarif_cubage_liege_femelle=TarifCubage.objects.filter(Essence=essence_object_liege_femelle)

                essence_object_liege_male=Essenceliège.objects.get(Nom=essence, canton=canton_object, Regime=regime_objet, Typeliège='liège male')
                tarif_cubage_liege_male=TarifCubage.objects.filter(Essence=essence_object_liege_male)
                essence_id=essence_object_liege_femelle.id
                
                context={
                    'tarif_cubage_femelle': tarif_cubage_liege_femelle,
                    'tarif_cubage_male': tarif_cubage_liege_male, 
                    'essence_id': essence_id

                }
                return render(request, 'Rendementliege/choix_tarif.html', context)
            except ObjectDoesNotExist as e:
                messageError="Le Chêne-liège qui possède ces critères de recherche n'existe pas dans la base de données"
                context = {
                    'form': form,
                    'message': messageError,
                    
                    
                    }
                return render(request, "Rendementliege/index.html", context)
            

                           

    else:
        form = TarifCubageForm()

    context = {'form': form}
    return render(request, "Rendementliege/index.html", context)

#____________________________________________________________________________________________________________________________________________________
def choixTarif_cubage_formulaire(request):
    if request.method == 'POST':
        nom_projet=request.POST.get('Nom_projet')
        liege_reproduction_id = request.POST.get('formule_liege_reproduction')
        liege_male_id = request.POST.get('formule_liege_male')
        liege_de_reproduction = TarifCubage.objects.get(id=liege_reproduction_id)
        liege_male = TarifCubage.objects.get(id=liege_male_id)
        operation_object=Operation_de_calcul_de_Rendement.objects.create(Nom=nom_projet, tarif_rendement_liege_reproduction=liege_de_reproduction,
                                                                                         tarif_rendement_liege_male=liege_male)
        operation_id=operation_object.id
        operationiobj=Operation_de_calcul_de_Rendement.objects.get(id=operation_id)
        formule_tarif_liege_de_reproduction = liege_de_reproduction.formule
        formule_tarif_liege_male=liege_male.formule
        circonf_min=liege_de_reproduction.circonference_min
        circonf_max=liege_de_reproduction.circonference_max

        #fonction calcul de volume
        def calculer_volume_liege(formule, circonference):
            formule_avec_virgule=formule
            formule_avec_point=formule_avec_virgule.replace(',', '.')
            C=circonference
            volume= eval(formule_avec_point)
            #COVERSION en m3, on le divise par 1000
            return volume/1000
        
        def calculer_volume_hause(circonfence_1m30):
             formule_volume_hausse='E*H*C'
             C=circonfence_1m30/100
             E=0.03
             H=0.2
             volume_hausse=eval(formule_volume_hausse)
             return volume_hausse
        


        for circonf in range(circonf_min, circonf_max + 1, 10):
                    volume_indivi_liege_reproduction = calculer_volume_liege(formule_tarif_liege_de_reproduction, circonf)
                    volume_indivi_liege_male = calculer_volume_liege(formule_tarif_liege_male, circonf)
                    volume_hausse_par_classe=calculer_volume_hause(circonf)

                    liege=liste_liege_par_Circonference.objects.create(operation_de_calcul_de_Rendement=operation_object, circonferance_1m30=circonf,
                    volume_individuel_liege_de_reproduction=volume_indivi_liege_reproduction, volume_individuel_liege_male=volume_indivi_liege_male,
                    volume_individuel_hausse=volume_hausse_par_classe, nombre_de_liege_de_reproduction_classe=0, nombre_de_liege_de_male_classe=0, 
                    volume_total_liege_de_reproduction_classe=0, volume_total_liege_de_male_classe=0)
                  
 





        liste_de_liege_par_operation=liste_liege_par_Circonference.objects.filter(operation_de_calcul_de_Rendement=operation_object).order_by('circonferance_1m30')

        context={
        "liste_de_liege_par_operation": liste_de_liege_par_operation,
        "operation_id":operation_id,
        'operation_objet': operationiobj,
    }
        return render(request, 'Rendementliege/informations.html', context)
    else:
        return redirect('Rendementliege:index')  

#__________________________________________________________________________________________________________________________________________________________

def operationformulaire(request, operation_id):
    #recuperation de l'objet operation liège  pour le remplissage automatique du formulaire
    operation_objet = get_object_or_404(Operation_de_calcul_de_Rendement, id=operation_id)

    if request.method == 'POST':
        form = OperationForm(request.POST, instance=operation_objet)
        if form.is_valid():
            form.save()
            context={
                'operation_id': operation_id, 
                'operation_objet':operation_objet, 

            }

            return render(request, 'Rendementliege/informations.html', context)     

    else:
        form = OperationForm(instance=operation_objet)

    context = {
        'form': form,
        'operation_id': operation_id,
        'operation_objet': operation_objet,
        
    }
    return render(request, "Rendementliege/operation _detail.html", context)   

#______________________________________________________________________________________________________________________________________________________________________

def calcul_rendement_liege(request, operation_id):
    operation_object = Operation_de_calcul_de_Rendement.objects.get(id=operation_id)

    liste_de_liege=liste_liege_par_Circonference.objects.filter(operation_de_calcul_de_Rendement=operation_object).order_by('circonferance_1m30')
    labels=[]
    NombreLR=[]
    NombreLM=[]
    volumelR=[]
    volumelM=[]
    
    for liege in liste_de_liege:
        labels.append(liege.circonferance_1m30)
        NombreLR.append(liege.nombre_de_liege_de_reproduction_classe)
        NombreLM.append(liege.nombre_de_liege_de_male_classe)
        volumelR.append(int(liege.volume_total_liege_de_reproduction_classe))
        volumelM.append(int(liege.volume_total_liege_de_male_classe))
    print(NombreLM)
    context={
        "liste_de_liege": liste_de_liege,

        'operation_id': operation_id,
        'operation_object': operation_object, 
        'labels': labels, 
        'NombreLR': NombreLR, 
        'NombreLM': NombreLM, 
        'volumelR': volumelR,
        'volumelM': volumelM,  

    }

    return render(request, "Rendementliege/liste_de_liege.html", context)

#______________________________________________________________________________________________________________________________________________________________

def formulaire_liste_liege(request, operation_id):
    
    operation_object = Operation_de_calcul_de_Rendement.objects.get(id=operation_id)

    
    if request.method == 'POST':
        for liege_id, nombre_liege_Reproduction, nombre_male in zip( request.POST.getlist('liege_id'), request.POST.getlist('nombre_liege_Reproduction'),request.POST.getlist('nombre_male') ):
            liege = liste_liege_par_Circonference.objects.get(id=liege_id)
            liege.nombre_de_liege_de_reproduction_classe= Decimal(nombre_liege_Reproduction)
            liege.nombre_de_liege_de_male_classe=Decimal(nombre_male)
            volume_liege_de_reproduction_individuel=liege.volume_individuel_liege_de_reproduction
            volume_liege_de_male_individuel=liege.volume_individuel_liege_male
            volume_hausse_individuel=liege.volume_individuel_hausse
            
            

            #calcule de volume total
            liege.volume_total_liege_de_reproduction_classe= volume_liege_de_reproduction_individuel*Decimal(nombre_liege_Reproduction)
            liege.volume_total_liege_de_male_classe=(volume_liege_de_male_individuel*Decimal(nombre_male))+ (volume_hausse_individuel*Decimal(nombre_liege_Reproduction))

            liege.save()
        return redirect('Rendementliege:calculRendement', operation_id) 
    
   
    liste_de_liege=liste_liege_par_Circonference.objects.filter(operation_de_calcul_de_Rendement=operation_object).order_by('circonferance_1m30')

    context={
        "liste_de_liege": liste_de_liege,

        'operation_id': operation_id
    }

    return render(request, "Rendementliege/liste_de_liege.html", context)

#__________________________________________________________________________________________________________________________________________________________________

def Calcul_somme_total_liege(request, operation_id):
    operation_object=Operation_de_calcul_de_Rendement.objects.get(id=operation_id)
    liste_de_liege=liste_liege_par_Circonference.objects.filter(operation_de_calcul_de_Rendement=operation_object)
    formule_LR = operation_object.tarif_rendement_liege_reproduction.formule
    formule_LM = operation_object.tarif_rendement_liege_male.formule
    essence = operation_object.tarif_rendement_liege_male.Essence.Nom
    liste_liege_de_reproduction_par_circonference=[]
    liste_liege_male_par_circonference=[]
    for liege in liste_de_liege:
        liste_liege_de_reproduction_par_circonference.append(liege.volume_total_liege_de_reproduction_classe)
        liste_liege_male_par_circonference.append(liege.volume_total_liege_de_male_classe)
    
    
         
    #volume total dans la placette
    if operation_object:
        volume_total_LR=sum(liste_liege_de_reproduction_par_circonference)
        volume_total_LM=sum(liste_liege_male_par_circonference)
        volumeTotal=volume_total_LR+volume_total_LM
        operation_object.volume_total_liege_de_reproduction=volume_total_LR
        operation_object.volume_total_liege_de_male=volume_total_LM
        operation_object.volume_total_de_liege=volumeTotal

        #information 
        tarif_object= operation_object.tarif_rendement_liege_reproduction
        essence_objet=tarif_object.Essence
        essencename=essence_objet.Nom
        Canton_object=essence_objet.canton
        canton_name=Canton_object.nom
        Foret=Canton_object.foret.nom
        regime=tarif_object.Essence.Regime.Nom

    

    


        context={
             'essence': essence, 
             'formule_LR':formule_LR,
             'formule_LM':formule_LM,
             'volume_total_LR':volume_total_LR,
             'volume_total_LM':volume_total_LM, 
             'volumeTotal':volumeTotal,
             'essencename':essencename,
             'canton_name':canton_name, 
             'Foret':Foret,
             'regime':regime,
             'liste_de_liege': liste_de_liege,
             'operation_object': operation_object,

        }
    
        return render(request, 'Rendementliege/resultat_rendement_liege.html', context)
    else:
        raise('il ya une erreur')

    
 #_________________________________________________________________________________________________________________________________
@login_required
def operation_list_rendement(request):
    operations_liste = Operation_de_calcul_de_Rendement.objects.all()

    return render(request, 'Rendementliege/operation_list.html', {'operations_liste': operations_liste})



def operation_delete(request, pk):
    operation = get_object_or_404(Operation_de_calcul_de_Rendement, pk=pk)
    if request.method == 'POST':
        operation.delete()
        return redirect('Rendementliege:operation_list_rendement')
    return render(request, 'Rendementliege/operation_confirm_delete.html', {'operation': operation})


def Consulter_info(request, pk):
    operation_objet = Operation_de_calcul_de_Rendement.objects.get(id=pk)
    operation_id=operation_objet.id
    context={
                'operation_objet': operation_objet, 
                'operation_id':operation_id,
            }

    return render(request,'Rendementliege/informations.html', context)
