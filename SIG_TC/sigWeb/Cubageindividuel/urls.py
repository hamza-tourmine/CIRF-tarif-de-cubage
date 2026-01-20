from django.urls import path

from . import views

app_name = "Cubageindividuel"

urlpatterns = [
    #/Cubagepeuplement/
    path("", views.index, name="index"),
    path("choixTarifcubage/<int:essence_id>", views.choixTarif_cubage_formulaire, name='choixtarifCubage'),
    path("Calculvolume_bois/<int:placette_id>", views.calculVolume_bois, name='Calcule'),
    path("formulaire_liste_de_bois/<int:placette_id>", views.formulaire_liste_bois, name='formulaire_liste_bois'),
    path("volume_total_liste_bois/<int:placette_id>", views.Calcul_somme_total_bois, name='volume_total'),
    path('strates_formulaire/<int:strate_id>/', views.strateformulaire, name="strate_form_individuel"),
    path('operation_liste/', views.operation_list_individuel, name="operation_list_individuel"),
     path('delete/<int:pk>/', views.operation_delete, name='operation_delete'),
    path('Consulet_info/<int:pk>/', views.Consulter_info, name='consult_info'),
    
]