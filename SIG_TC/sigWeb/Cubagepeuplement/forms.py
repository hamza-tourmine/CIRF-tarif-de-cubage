from django import forms 
from .models import *


#formulaire pour la recherche du tarifs de cubage
class TarifCubageForm(forms.Form):
    foret = forms.ModelChoiceField(queryset=Foret.objects.all().order_by('nom'),
                                   widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'})
    )
    canton = forms.ModelChoiceField(queryset=Canton.objects.all().order_by('nom'), empty_label="Sélectionnez un canton",widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))

    especeexistant = [("Sélectionnez une essence","Sélectionnez une essence"),
                      ('Acacia mearnsii', 'Acacia mearnsii'),  
                      ('Eucalyptus camaldulensis', 'Eucalyptus camaldulensis'),
                      ('Eucalyptus clonal', 'Eucalyptus clonal'),
                      ('Eucalyptus grandis', 'Eucalyptus grandis'),
                      ('Pin maritime', 'Pin maritime'),


                      ]
    
    essence = forms.ChoiceField(choices=especeexistant,widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    regime = forms.ModelChoiceField(queryset=Regime.objects.all(), empty_label="Sélectionnez un régime",widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    


#formulaire pour la recherche du tarifs de cubage

class StratesForm(forms.ModelForm):
    class Meta:
        model = Strate
        fields = ['Superficie_de_la_strate', 'nombre_placette','parcelle', 'groupe']


class PlacetteForm(forms.ModelForm):
    class Meta:
        model = Placette
        fields = ['Profondeur_de_sol']
    


class liste_de_boisForm(forms.ModelForm):
    class Meta:
        model=liste_de_bois
        fields=['circonferance_1m30', 'volume_individuel', 'nombre_de_bois_classe','volume_total_classe']


class choixTarifCubageForm(forms.Form):
    def __init__(self, *args, essence=None, **kwargs):
        super().__init__(*args, **kwargs)
        if essence:
            tarifcubages = TarifCubage.objects.filter(Essence=essence)
            tariff_choices = []
            for tariff in tarifcubages:
                label = f"{tariff.formule}"
                choice = (tariff.id, label)
                tariff_choices.append(choice)
            self.fields['tarif_de_cubage'] = forms.ChoiceField(choices=tariff_choices,widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))

    Nom_projet=forms.CharField(label='Nom du projet', widget=forms.TextInput(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    TypeEchantillonage=forms.ModelChoiceField(queryset=TypeEchantillonage.objects.all().order_by('Nom'), empty_label="Sélectionnez le type d'echantillonnage", label="Type d'échantillonage",widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    superficie_peuplement=forms.DecimalField(label="Superficie du peuplement", widget=forms.TextInput(attrs={'placeholder': 'Unité de mesure en hectare','class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    Nombre_de_strate=forms.IntegerField(label="Nombre de strate", initial=1,widget=forms.TextInput(attrs={'placeholder': 'Unité de mesure en ares','class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    surface_de_la_placette = forms.IntegerField(label="Surface de la placette", widget=forms.TextInput(attrs={'placeholder': 'Unité de mesure en ares','class': 'custom-select', 'style': 'border: 2px solid Green;'}))

class OperationDeCalculForm(forms.ModelForm):
    class Meta:
        model = Operation_de_calcul
        fields = '__all__'