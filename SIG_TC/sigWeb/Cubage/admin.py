from django.contrib import admin
from .models import *

# Register your models here.


class ForetAdmin(admin.ModelAdmin):
    list_display=('nom','superficie')
    search_fields=['nom',]

class CantonAdmin(admin.ModelAdmin):
    list_display=('nom','superficie','foret')
    search_fields=['nom',]
    list_filter=['nom', 'foret']

class SerieAdmin(admin.ModelAdmin):
    list_display=('nom','superficie','foret')
    search_fields=['nom',]
    list_filter=['nom', 'foret']

class GroupemamoraAdmin(admin.ModelAdmin):
    list_display=('nom_groupe','serie', )
    search_fields=['nom_groupe',]
    list_filter=['nom_groupe', 'serie']

class DRANEFAdmin(admin.ModelAdmin):
    list_display=('nom','superficie', )
    search_fields=['nom',]
    
class DPANEFAdmin(admin.ModelAdmin):
    list_display=('nom','superficie','DRANEF' )
    search_fields=['nom',]
    list_filter=['nom', 'DRANEF']

class ZDTFAdmin(admin.ModelAdmin):
    list_display=('nom','superficie','DPANEF' )
    search_fields=['nom',]
    list_filter=['nom', 'DPANEF']

class DFPAdmin(admin.ModelAdmin):
    list_display=('nom','superficie','ZDTF' )
    search_fields=['nom',]
    list_filter=['nom', 'ZDTF']

from django.contrib import admin

class ParcellaireAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information sur les découpage à laquelle appartiennent la parcelle', {
            'fields': ('commune', 'canton', 'DFP', 'groupe')
        }),
        ('Information sur la parcelle', {
            'fields': ('parcelle', 'Description', 'limite_Nord', 'limite_Sud', 'limite_Est', 'limite_ouest')
        }),
        ('Information sur la geometrie', {
            'fields': ('geom', 'shape_leng', 'shape_area')
        }),
    ]

    list_display=('parcelle','groupe','canton', 'DFP', 'commune')
    list_filter=['parcelle', 'groupe','canton','DFP', 'commune']


class EssencesAdmin(admin.ModelAdmin):
    list_display=('Nom','Regime','canton' )
    search_fields=['Nom',]
    list_filter=['Nom', 'Regime','canton']
class EssencesliegeAdmin(admin.ModelAdmin):
    list_display=('Nom','Regime','canton', 'Typeliège' )
    search_fields=['Nom',]
    list_filter=['Nom', 'Regime','canton','Typeliège']

class TarifAdmin(admin.ModelAdmin):
    list_display=('formule','typeVolume','Essence' )
    search_fields=['Essence',]
    list_filter=['Essence', 'typeVolume']

class Operation_de_calculAdmin(admin.ModelAdmin):
    list_display=('Nom', )
    search_fields=['Nom',]




admin.site.register(Foret, ForetAdmin)
admin.site.register(Canton, CantonAdmin)
admin.site.register(Serie,SerieAdmin)
admin.site.register(Groupemamora,GroupemamoraAdmin)
admin.site.register(Regions)
admin.site.register(Provinces)
admin.site.register(Communes)
admin.site.register(DRANEF, DRANEFAdmin)
admin.site.register(DPANEF, DPANEFAdmin)
admin.site.register(ZDTF, ZDTFAdmin)
admin.site.register(DFP)
admin.site.register(Parcellaire, ParcellaireAdmin)


admin.site.register(Essences,EssencesAdmin)
admin.site.register(Essenceliège, EssencesliegeAdmin)
admin.site.register(Regime)
admin.site.register(TarifCubage,TarifAdmin)

admin.site.register(TypeEchantillonage)
admin.site.register(Operation_de_calcul,Operation_de_calculAdmin)
admin.site.register(Operation_de_calcul_de_Rendement,Operation_de_calculAdmin)


