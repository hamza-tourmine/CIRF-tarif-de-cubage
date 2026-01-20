from django.urls import path

from . import views

app_name = "Cubagepeuplement"

urlpatterns = [
    #/Cubagepeuplement/
    path("", views.index, name="index"),
    path('strates/<int:operation_id>/', views.strateview, name="strates"),
    path('strates_formulaire/<int:strate_id>/', views.strateformulaire, name="strate_form"),
    path('placette/<int:strate_id>/', views.placetteview, name="placettes"),
    path('liste_bois/<int:placette_id>/', views.liste_boisview, name="liste_bois"),
    path('calcul_de_volume/<int:placette_id>/', views.calcul_volume_bois_par_placette, name="calcul_volume"), 
    path('calcul_volume_totat_par_placette/<int:placette_id>/', views.Calcul_somme_total_bois_ha_par_placette, name="volume_total_ha"),
    path('calcul_volume_moyenne_et total_estimé_par_strate/<int:strate_id>/', views.Calcul_volume_moyen_et_total_bois_ha_par_strate_id, name="volume_par_strate"),
    path('resulat_echatillonage_al_stratitife/<int:operation_id>/', views.calcul_volume_peuplement, name="volume_peup_echn_aleatoire_strat"),
    path("choixTarifcubage/<int:essence_id>", views.choixTarif_cubage_formulaire, name='choixtarifCubage'),
    path("liste_arbre/<int:placette_id>", views.formulaire_liste_bois, name='liste_arbre'),
    path('placette_formulaire/<int:Placette_id>/', views.Placetteformulaire, name="placette_form"),
    path('operation_liste/', views.operation_list, name="operation_list_peuplement"),
    path('delete/<int:pk>/', views.operation_delete, name='operation_delete'),

    

]

