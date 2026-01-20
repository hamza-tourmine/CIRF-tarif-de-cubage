from django.urls import path

from . import views

app_name = "Rendementliege"

urlpatterns = [
    
    path("", views.index, name="index"),
    path("traitement_des_tarif_choisi/", views.choixTarif_cubage_formulaire, name='create_operation'),
    path("liste_liege/<int:operation_id>", views.calcul_rendement_liege, name='calculRendement'),
    path("liste_arbre_liege/<int:operation_id>", views.formulaire_liste_liege, name='liste_arbre'),
    path("resulat_liege/<int:operation_id>", views.Calcul_somme_total_liege, name='Resulat'),
    path('operation_formulaire/<int:operation_id>/', views.operationformulaire, name="operation_form_individuel"),
    path('operation_liste/', views.operation_list_rendement, name="operation_list_rendement"),
    path('delete/<int:pk>/', views.operation_delete, name='operation_delete'),
    path('Consulet_info/<int:pk>/', views.Consulter_info, name='consult_info'),
    
]
