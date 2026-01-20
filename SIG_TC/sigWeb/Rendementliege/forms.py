from django import forms 
from .models import *


#formulaire pour la recherche du tarifs de cubage
class TarifCubageForm(forms.Form):
    foret = forms.ModelChoiceField(queryset=Foret.objects.all().order_by('nom'), empty_label="Sélectionnez une forêt", widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    canton = forms.ModelChoiceField(queryset=Canton.objects.all().order_by('nom'), empty_label="Sélectionnez un canton", widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))

    especeexistant = [
                      ('Chêne-liège', 'Chêne-liège'),


                      ]
    
    essence = forms.ChoiceField(choices=especeexistant,widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    regime = forms.ModelChoiceField(queryset=Regime.objects.all(), empty_label="Sélectionnez un régime", widget=forms.Select(attrs={'class': 'custom-select', 'style': 'border: 2px solid Green;'}))
    

#formulaire pour la recherche du tarifs de cubage







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
            self.fields['tarif_de_cubage_male'] = forms.ChoiceField(choices=tariff_choices)
            self.fields['tarif_de_cubage_femmelle'] = forms.ChoiceField(choices=tariff_choices)

    
    
    
class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation_de_calcul_de_Rendement
        fields = ['parcelle', 'groupe', 'Annee_de_demasclage']