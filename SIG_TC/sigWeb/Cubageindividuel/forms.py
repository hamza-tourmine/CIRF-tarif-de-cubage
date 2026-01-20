from django import forms 
from .models import *


#formulaire pour la recherche du tarifs de cubage
class TarifCubageForm(forms.Form):
    foret = forms.ModelChoiceField(queryset=Foret.objects.all().order_by('nom'), empty_label="Sélectionnez une forêt", widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    canton = forms.ModelChoiceField(queryset=Canton.objects.all().order_by('nom'), empty_label="Sélectionnez un canton", widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))

    especeexistant = [("Sélectionnez une essence","Sélectionnez une essence"),
                      ('Acacia mearnsii', 'Acacia mearnsii'),  
                      ('Eucalyptus camaldulensis', 'Eucalyptus camaldulensis'),
                      ('Eucalyptus clonal', 'Eucalyptus clonal'),
                      ('Eucalyptus grandis', 'Eucalyptus grandis'),
                      ('Pin maritime', 'Pin maritime'),


                      ]
    
    essence = forms.ChoiceField(choices=especeexistant,widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    regime = forms.ModelChoiceField(queryset=Regime.objects.all(), empty_label="Sélectionnez un régime",widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))


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
            self.fields['tarif_de_cubage'] = forms.ChoiceField(choices=tariff_choices, widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    Nom_projet=forms.CharField(label='Nom du projet',  widget=forms.TextInput(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
            


class liste_de_boisForm(forms.ModelForm):
    class Meta:
        model=liste_de_bois
        fields=['circonferance_1m30', 'nombre_de_bois_classe','volume_individuel',  'volume_total_classe']


class StratesForm(forms.ModelForm):
    class Meta:
        model = Strate
        fields = ['parcelle', 'groupe']


class OperationDeCalculForm(forms.ModelForm):
    class Meta:
        model = Operation_de_calcul
        fields = '__all__'