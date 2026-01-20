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

            # Récupération des objets associés aux choix du formulaire
            try:
                foret_objets = Foret.objects.get(nom=foret)
                canton_object = Canton.objects.get(nom=canton, foret=foret_objets)
                regime_objet = Regime.objects.get(Nom=regime)
                essence_object=Essences.objects.get(Nom=essence, canton=canton_object, Regime=regime_objet)
                essence_id=essence_object.id

                return redirect('Cubagepeuplement:choixtarifCubage', essence_id)
            except ObjectDoesNotExist as e:
                messageError="L'essence qui possède ces critères de recherche n'existe pas dans la base de données"
                context = {
                    'form': form,
                    'message': messageError,
                    
                    
                    }
                return render(request, "Cubagepeuplement/index.html", context)
            

                           

    else:
        form = TarifCubageForm()

    context = {'form': form}
    return render(request, "Cubagepeuplement/index.html", context)

#____________________________________________________________________________________________________________________________________________________
def choixTarif_cubage_formulaire(request, essence_id):
    essence_object = Essences.objects.get(id=essence_id)


    if request.method == 'POST':
        form = choixTarifCubageForm(request.POST, essence=essence_object)
        if form.is_valid():
            tarif_cubage_selectionner = form.cleaned_data['tarif_de_cubage']
            TypeEchantillonages=form.cleaned_data['TypeEchantillonage']
            surface_de_la_placette=form.cleaned_data['surface_de_la_placette']
            Nombre_de_strate=form.cleaned_data['Nombre_de_strate']
            superficie_du_peuplement=form.cleaned_data['superficie_peuplement']
            Nom_projet=form.cleaned_data['Nom_projet']
            # Récupération du tarif de cubage
            tarif_cubage=None
            tarif_cubage = TarifCubage.objects.get(id=tarif_cubage_selectionner)
            print(tarif_cubage)


            # Création de l'opération de calcul
            TypeEchantillonage_object= TypeEchantillonage.objects.get(Nom=TypeEchantillonages)

            operation_objet=Operation_de_calcul.objects.create(TarifCubage=tarif_cubage, TypeEchantillonage=TypeEchantillonage_object, 
                                                               Surface_de_placette=surface_de_la_placette, Nombre_de_strate=Nombre_de_strate, 
                                                               superficie_peuplement=superficie_du_peuplement, Nom=Nom_projet)
            
            # Création des strates associées à l'opération et redirection vers une page selon le type d'echantillonnage
            nombre_de_strates=operation_objet.Nombre_de_strate

            if TypeEchantillonage_object.Nom=="Echantillonnage aléatoire stratifié":
                for i in range(nombre_de_strates):
                    num=i+1
                    strate = Strate(Operation_de_calcul=operation_objet,numero=num, Superficie_de_la_strate=0, nombre_placette=0,
                                    volume_moyenne_strate=0, volume_total_strate=0, ecart_type_strate=0, erreur_standard=0)
                    strate.save()
                
                return redirect("Cubagepeuplement:strates", operation_id=operation_objet.id)
            
            elif TypeEchantillonage_object.Nom=='Echantillonnage aléatoire simple' or TypeEchantillonage_object.Nom=='Echantillonnage systématique':
                for i in range(nombre_de_strates):
                    strate = Strate(Operation_de_calcul=operation_objet, numero=i, Superficie_de_la_strate=superficie_du_peuplement, nombre_placette=0,
                                    volume_moyenne_strate=0, volume_total_strate=0, ecart_type_strate=0, erreur_standard=0)
                    strate.save()
                return redirect("Cubagepeuplement:strates", operation_id=operation_objet.id)
            else:
                raise('error')
            
            

    else:
        form = choixTarifCubageForm(essence=essence_object)

    context = {
        'form': form,
    }

    return render(request, 'Cubagepeuplement/choix_tarif.html', context)

#__________________________________________________________________________________________________________________________________________________________

#vue pour l'affichage des strates
def strateview(request, operation_id):
    operation_object=Operation_de_calcul.objects.get(id=operation_id)

    strates=Strate.objects.filter(Operation_de_calcul=operation_object).order_by('id')

    typeEchantillonage=operation_object.TypeEchantillonage.Nom
 
    context={
        'strates':strates,
        'operation_id':  operation_id,
        'type_echantillonnage': typeEchantillonage,

    }
    return render(request, "Cubagepeuplement/strates.html", context)

#____________________________________________________________________________________________________________________________________________________________

#vue pour afficher chaque strate et creation des objets placette 


def strateformulaire(request, strate_id):
    #recuperation de l'objet strate pour le remplissage automatique du formulaire
    strate_objet = get_object_or_404(Strate, id=strate_id)
    #recuperation de l'objet operation pour le redirect vers les strates 
    operation_objet=strate_objet.Operation_de_calcul

    if request.method == 'POST':
        form = StratesForm(request.POST, instance=strate_objet)
        if form.is_valid():
            form.save()
            nombre_de_placette=strate_objet.nombre_placette
            for i in range(nombre_de_placette):
                num=i+1
                placette = Placette(Strate=strate_objet, numero_placette=num, volume_total=0, volume_hectares=0)
                placette.save()
            return redirect("Cubagepeuplement:strates", operation_objet.id)     

    else:
        form = StratesForm(instance=strate_objet)

    context = {
        'form': form,
        'strate': strate_objet,
    }
    return render(request, "Cubagepeuplement/strates_detail.html", context)

#__________________________________________________________________________________________________________________________________________________________

#vue pour accéder les placettes associé a une strate

def placetteview(request, strate_id):
    strate_object=Strate.objects.get(id=strate_id)

    Placettes=Placette.objects.filter(Strate=strate_object).order_by('id')
    labels=[]
    volume=[]

    for placette in Placettes:
        labels.append(placette.numero_placette)

        volume.append(int(placette.volume_hectares))
 
    context={
        'Placettes':Placettes,
        'strate_id': strate_id,
        'volume': volume, 
        'labels': labels

    }
    return render(request, "Cubagepeuplement/placettes.html", context)


#________________________________________________________________________________________________________________________________________________________________________________________

def liste_boisview(request, placette_id):

    # Trouver la placette correspondante
    placette = Placette.objects.get(pk=placette_id)

    # Accéder au tarif de cubage associé
    tarif_cubage = placette.Strate.Operation_de_calcul.TarifCubage
    
    #  vous pouvez obtenir la formule du tarif de cubage, circonference min et max
    formule_tarif = tarif_cubage.formule
    circonf_min=tarif_cubage.circonference_min
    circonf_max=tarif_cubage.circonference_max

    #fonction calcul de volume
    def calculer_volume(formule, circonference):
        formule_avec_virgule=formule
        formule_avec_point=formule_avec_virgule.replace(',', '.')
        C=circonference
        volume= eval(formule_avec_point)
        #COVERSION en m3, on le divise par 1000
        return volume/1000
    
    Lettre='h'
    presence_hauteur=None
    if Lettre in formule_tarif.lower():
        presence_hauteur=True
        for circonf in range(circonf_min, circonf_max + 1, 10):
                    bois=liste_de_bois.objects.create(Placette=placette,  circonferance_1m30=circonf, 
                                                    volume_individuel=0, nombre_de_bois_classe=0,
                                                    volume_total_classe=0, hauteur=0 )
    else:
        presence_hauteur=False
        for circonf in range(circonf_min, circonf_max + 1, 10):
                volume_par_classe = calculer_volume(formule_tarif, circonf)
                bois=liste_de_bois.objects.create(Placette=placette, circonferance_1m30=circonf, 
                                                volume_individuel=volume_par_classe, nombre_de_bois_classe=0,
                                                volume_total_classe=0 )


    liste_de_bois_par_placette=liste_de_bois.objects.filter(Placette=placette).order_by('circonferance_1m30')

    labels=[]
    Nombrebois=[]
    volumebois=[]
    
    for bois in liste_de_bois_par_placette:
        labels.append(bois.circonferance_1m30)
        Nombrebois.append(bois.nombre_de_bois_classe)
        volumetot=int(bois.volume_total_classe)
        volumebois.append(volumetot)

    context={
        "liste_de_bois_par_placette": liste_de_bois_par_placette,
        "placette_id":placette_id,
        'presence_hauteur': presence_hauteur,
        'labels': labels,
        'Nombrebois': Nombrebois,
        'volumebois': volumebois,
    }
    return render(request, "Cubagepeuplement/liste_de_bois.html", context)

#________________________________________________________________________________________________________________________________________________________________________________

def calcul_volume_bois_par_placette(request, placette_id):
    placette = Placette.objects.get(pk=placette_id)
    liste_de_bois_par_placette=liste_de_bois.objects.filter(Placette=placette).order_by('circonferance_1m30')
    formule=placette.Strate.Operation_de_calcul.TarifCubage.formule
    Lettre='h'
    presence_hauteur=None
    if Lettre in formule.lower():
        presence_hauteur=True
    else:
        presence_hauteur=False

    labels=[]
    Nombrebois=[]
    volumebois=[]
    
    for bois in liste_de_bois_par_placette:
        labels.append(bois.circonferance_1m30)
        Nombrebois.append(bois.nombre_de_bois_classe)
        volumetot=int(bois.volume_total_classe)
        volumebois.append(volumetot)
    

    context={
        "liste_de_bois_par_placette": liste_de_bois_par_placette,
        "placette_id":placette_id,
        'presence_hauteur': presence_hauteur,
        'labels': labels,
        'Nombrebois': Nombrebois,
        'volumebois': volumebois, 
    }

    return render(request, "Cubagepeuplement/liste_de_bois.html", context)


#__________________________________________________________________________________________________________________________________________________________________________________________

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
            return redirect('Cubagepeuplement:calcul_volume', placette_id) 
    else:
        if request.method == 'POST':
            for bois_id, nombre_bois in zip( request.POST.getlist('bois_id'), request.POST.getlist('nombre_bois')):
                bois = liste_de_bois.objects.get(id=bois_id)
                bois.nombre_de_bois_classe= Decimal(nombre_bois)
            
                volumeindi= bois.volume_individuel
                bois.volume_total_classe = Decimal(nombre_bois)*volumeindi
                bois.save()
            return redirect('Cubagepeuplement:calcul_volume', placette_id)

    placette = Placette.objects.get(pk=placette_id)
    liste_de_bois_par_placette=liste_de_bois.objects.filter(Placette=placette).order_by('circonferance_1m30')

    
    context={
        "liste_de_bois_par_placette": liste_de_bois_par_placette,
        "placette_id":placette_id,
    
    }
    return render(request, 'Cubagepeuplement/liste_de_bois.html', context)



#_____________________________________________________________________________________________________________________________________________________________________________________________

def Calcul_somme_total_bois_ha_par_placette(request, placette_id):
    placette = Placette.objects.get(pk=placette_id)
    strate_id=placette.Strate.id
    surface_de_la_placette=Decimal(placette.Strate.Operation_de_calcul.Surface_de_placette)
    liste_de_bois_par_placette=liste_de_bois.objects.filter(Placette=placette)
    liste_volume_total_par_circonference=[]
    for bois in liste_de_bois_par_placette:
        liste_volume_total_par_circonference.append(bois.volume_total_classe)
         
    #volume total dans la placette
    if placette:
        volume_total_par_placette=sum(liste_volume_total_par_circonference)
        placette.volume_total=volume_total_par_placette
    #volume à l'hectare dans la placette
        placette.volume_hectares=volume_total_par_placette*(100/surface_de_la_placette)
        placette.save()
        return redirect('Cubagepeuplement:placettes', strate_id)
    else:
        raise('il ya une erreur')

#______________________________________________________________________________________________________________________________________________________________________

def Calcul_volume_moyen_et_total_bois_ha_par_strate_id(request, strate_id):
    strate = Strate.objects.get(pk=strate_id)
    operation_id=strate.Operation_de_calcul.id
    superficie_de_la_strate=Decimal(strate.Superficie_de_la_strate)
    liste_de_placette_par_strate=Placette.objects.filter(Strate=strate)

    #donnée d'echantillon
    liste_volume_total_hectare_par_placette=[]
    for placette in liste_de_placette_par_strate:
        liste_volume_total_hectare_par_placette.append(placette.volume_hectares)
         
    
    if strate:
        moyenne = Decimal(np.mean(liste_volume_total_hectare_par_placette))
        taille_echantillon = len(liste_volume_total_hectare_par_placette)
        ecart_type_echantillon = Decimal(np.std(liste_volume_total_hectare_par_placette, ddof=1))
        erreur_echantillonnage = ecart_type_echantillon / Decimal(np.sqrt(taille_echantillon))
        intervalle_confiances = stats.t.interval(0.95, df=float(taille_echantillon)-1, loc=float(np.mean(liste_volume_total_hectare_par_placette)), scale=float(erreur_echantillonnage))
        
        #volume moyenne estimé de la strate
        strate.volume_moyenne_strate=moyenne
        #volume total estmié de la strate
        strate.volume_total_strate=moyenne*superficie_de_la_strate
        #parametre statistique
        strate.ecart_type_strate=ecart_type_echantillon
        strate.erreur_standard=erreur_echantillonnage
        #intervalle confience
        strate.intervalle_confience = f'({round(intervalle_confiances[0], 3)}, {round(intervalle_confiances[1],3)})'
        
        strate.save()

        print('moyenne:', strate.volume_moyenne_strate)
        print('volume total strate:', strate.volume_total_strate)
        print("ecartype de l'echantillon:",strate.ecart_type_strate )
        print("ecartype de moyenne:", strate.erreur_standard)
        print("intervalle de confience:", strate.intervalle_confience)



        return redirect('Cubagepeuplement:strates', operation_id)
    
    else:
        raise('il ya un erreur')


#_________________________________________________________________________________________________________________________________________________________

def calcul_volume_peuplement(request, operation_id):
    strates=Strate.objects.filter(Operation_de_calcul=operation_id).order_by('numero')
    operation_de_calcul=Operation_de_calcul.objects.get(id=operation_id)

    superfecie_de_peuplement=operation_de_calcul.superficie_peuplement
    donne_strate_volume_moyenne_muliplier_par_superfice_par_strate=[]
    donnée_proportion_au_carre_mutiplier_par_erreur_standard_par_strate=[]

    placettes_by_strate = {}
    for strate in strates:
        Strate_superficie = strate.Superficie_de_la_strate
        strate_volume_moyenne = strate.volume_moyenne_strate
        proportion = Strate_superficie / superfecie_de_peuplement
        erreur_standard = strate.erreur_standard
        proprortion_erreur_standard = (proportion ** 2) * (erreur_standard ** 2)
        donne_strate_volume_moyenne_muliplier_par_superfice_par_strate.append(Strate_superficie * strate_volume_moyenne)
        donnée_proportion_au_carre_mutiplier_par_erreur_standard_par_strate.append(proprortion_erreur_standard)
        print(erreur_standard)
        print(strate.intervalle_confience)

        
        placettes_by_strate[strate] = Placette.objects.filter(Strate=strate)
        for placette in placettes_by_strate[strate]:
            liste_nombre_bois_placette = []
            liste_bois = liste_de_bois.objects.filter(Placette=placette)
            for bois in liste_bois:
                nombre_bois_classe = bois.nombre_de_bois_classe
                liste_nombre_bois_placette.append(nombre_bois_classe)

            placette.nombre_de_bois_total = sum(liste_nombre_bois_placette)




    if operation_de_calcul:
        #Volume du peuplement
        volume_moyenne_peuplement_hectare=sum(donne_strate_volume_moyenne_muliplier_par_superfice_par_strate)/superfecie_de_peuplement
        volume_total_du_peuplent=volume_moyenne_peuplement_hectare*superfecie_de_peuplement

        #ecartype de la moyenne du peuplement(moyenne generale)
        varience_moyenne_peuplement=sum(donnée_proportion_au_carre_mutiplier_par_erreur_standard_par_strate)
        ecart_type_moyenne_peuplement=Decimal(math.sqrt(varience_moyenne_peuplement))
        #erreur_type_relative
        erreur_type_relative=(ecart_type_moyenne_peuplement/volume_moyenne_peuplement_hectare)*100

        #sauvegarde des resulat dans la base données
        operation_de_calcul.volume_moyenne_peuplement_hectare=round(volume_moyenne_peuplement_hectare,3)
        operation_de_calcul.varience_moyenne=round(varience_moyenne_peuplement,3)
        operation_de_calcul.volume_total_du_peuplent=round(volume_total_du_peuplent,3)
        operation_de_calcul.ecart_type_moyenn=round(ecart_type_moyenne_peuplement, 3)
        operation_de_calcul.erreur_type_relative=round(erreur_type_relative,3)
        operation_de_calcul.save()

        #recuperation des données 
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
        
        print('nombre de strate:', len(strates))

        nombre_strate=len(strates)

        context={
            'resulat_peuplement': operation_de_calcul, 
            'essence': essencename,
            'canton_name':canton_name,
            'Foret':Foret,
            'regime':regime,
            'FormuleTarif': tarif_cubage_utilise,
            'intervalle_validite': intervalle_de_validite,
            'superfice_peuplement': superfecie_de_peuplement,
            'strates':strates,
            'placettes_by_strate':placettes_by_strate,
            'nombre_strate': nombre_strate,
        }

        return render(request, "Cubagepeuplement/resulat_echantillonnage_A_stratifie.html", context)
    
    else:
        raise('il ya un erreur')

    
        
#____________________________________________________________________________________________________________________________________________________________

def Placetteformulaire(request, Placette_id):
    #recuperation de l'objet placette pour le remplissage automatique du formulaire
    placette_objet = get_object_or_404(Placette, id=Placette_id)
    #recuperation de l'objet strate pour le redirect vers les placette 
    Strate_objet=placette_objet.Strate

    if request.method == 'POST':
        form = PlacetteForm(request.POST, instance=placette_objet)
        if form.is_valid():
            form.save()
            return redirect("Cubagepeuplement:placettes", Strate_objet.id)     

    else:
        form = PlacetteForm(instance=placette_objet)

    context = {
        'form': form,
        'placette': placette_objet,
    }
    return render(request, "Cubagepeuplement/placette_detail.html", context)

#___________________________________________________________________________________________________________________________________________________________
@login_required
def operation_list(request):
    operations_liste = Operation_de_calcul.objects.exclude(TypeEchantillonage__id='4')
    return render(request, 'Cubagepeuplement/operation_list.html', {'operations_liste': operations_liste})



def operation_delete(request, pk):
    operation = get_object_or_404(Operation_de_calcul, pk=pk)
    if request.method == 'POST':
        operation.delete()
        return redirect('Cubagepeuplement:operation_list_peuplement')
    return render(request, 'Cubagepeuplement/operation_confirm_delete.html', {'operation': operation})



