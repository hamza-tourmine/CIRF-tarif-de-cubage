from django.contrib.gis.db import models

# Create your models here.
#modele des données de la division  forestiere

class Foret(models.Model):
    nom = models.CharField(max_length=21, blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    superficie = models.FloatField(blank=True, null=True)


    def __str__(self):
        return self.nom

    class Meta:
        managed = True
        db_table = 'foretmaamora'
        verbose_name="Forêt"
        verbose_name_plural="Forêts"
    
     


class Canton(models.Model):
    foret = models.ForeignKey(Foret, on_delete=models.DO_NOTHING, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)
    nom = models.CharField(max_length=20, blank=True, null=True)
    superficie = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        managed = True
        db_table = 'canton'
        verbose_name="Canton"
        verbose_name_plural="Cantons"

class Serie(models.Model):
    foret = models.ForeignKey(Foret, on_delete=models.DO_NOTHING, null=True)
    nom = models.CharField(max_length=20, blank=True, null=True)
    superficie = models.FloatField(blank=True, null=True)
    revolution= models.FloatField(blank=True, null=True)


    def __str__(self):
        return self.nom

    class Meta:
        verbose_name="Serie"
        verbose_name_plural="Series"




class Groupemamora(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.DO_NOTHING,null=True )
    layer_id = models.FloatField(blank=True, null=True)
    layer = models.CharField(max_length=14, blank=True, null=True)
    nom_groupe = models.CharField(max_length=20, blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    geom = models.MultiPolygonField(blank=True, null=True)


    def __str__(self):
        return self.nom_groupe

    class Meta:
        managed = True
        db_table = 'groupemamora'
        verbose_name="Groupe"
        verbose_name_plural="Groupes"

# models de données decoupage administrative
        
class Regions(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    objectid = models.IntegerField(blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    nom = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        managed = True
        db_table = 'regions'
        verbose_name="Region"
        verbose_name_plural="Regions"

class Provinces(models.Model):
    region= models.ForeignKey(Regions, on_delete=models.DO_NOTHING,null=True )
    geom = models.MultiPolygonField(blank=True, null=True)
    objectid_1 = models.IntegerField(blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.nom

    class Meta:
        managed = True
        db_table = 'provinces'
        verbose_name="Province"
        verbose_name_plural="Provinces"

class Communes(models.Model):
    province = models.ForeignKey(Provinces, on_delete=models.DO_NOTHING,null=True )
    geom = models.MultiPolygonField(blank=True, null=True)
    objectid = models.IntegerField(blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)


    def __str__(self):
        return self.nom

    class Meta:
        managed = True
        db_table = 'communes'
        verbose_name="Commune"
        verbose_name_plural="Communes"
#modèle de données des decoupage de gestion

class DRANEF(models.Model):
    
    nom = models.CharField(max_length=100, blank=True, null=True)
    siege = models.CharField(max_length=100, blank=True, null=True)
    superficie = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.nom
    class Meta:
        verbose_name="DRANEF"
        verbose_name_plural="DRANEF"

class DPANEF(models.Model):
    DRANEF = models.ForeignKey(DRANEF, on_delete=models.DO_NOTHING,null=True )
    nom = models.CharField(max_length=100, blank=True, null=True)
    siege = models.CharField(max_length=100, blank=True, null=True)
    superficie = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.nom
    class Meta:
        verbose_name="DPANEF"
        verbose_name_plural="DPANEF"

class ZDTF(models.Model):
    DPANEF = models.ForeignKey(DPANEF, on_delete=models.DO_NOTHING,null=True )
    nom = models.CharField(max_length=100, blank=True, null=True)
    siege = models.CharField(max_length=100, blank=True, null=True)
    superficie = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.nom
    class Meta:
        verbose_name="ZDTF"
        verbose_name_plural="ZDTF"

class DFP(models.Model):
    ZDTF = models.ForeignKey(ZDTF, on_delete=models.DO_NOTHING,null=True )
    nom = models.CharField(max_length=100, blank=True, null=True)
    siege = models.CharField(max_length=100, blank=True, null=True)
    superficie = models.FloatField(blank=True, null=True)


    def __str__(self):
        return self.nom
    class Meta:
        verbose_name="DFP"
        verbose_name_plural="DFP"

#Modèle des données Parcellaire

class Parcellaire(models.Model):
    geom = models.MultiPolygonField(blank=True, null=True)
    parcelle = models.IntegerField(blank=True, null=True)
    limite_Nord = models.CharField(max_length=100, blank=True, null=True)
    limite_Sud = models.CharField(max_length=100, blank=True, null=True)
    limite_Est = models.CharField(max_length=100, blank=True, null=True)
    limite_ouest = models.CharField(max_length=100, blank=True, null=True)
    limite_Est= models.CharField(max_length=100, blank=True, null=True)
    Description= models.CharField(max_length=100, blank=True, null=True)
    shape_leng = models.FloatField(blank=True, null=True)
    shape_area = models.FloatField(blank=True, null=True)
    canton= models.ForeignKey(Canton, on_delete=models.DO_NOTHING, null=True)
    groupe= models.ForeignKey(Groupemamora, on_delete=models.DO_NOTHING, null=True)
    commune = models.ForeignKey(Communes, on_delete=models.DO_NOTHING,null=True )
    DFP = models.ForeignKey(DFP, on_delete=models.DO_NOTHING,null=True )


    def __str__(self):
        return f"{self.parcelle} - {self.groupe}-{self.canton} - {self.commune} - {self.DFP}"
    

    class Meta:
        managed = True
        db_table = 'parcellaire'
        verbose_name="Parcellaire"
        verbose_name_plural="Parcellaires"

#Modèle des données essence-tarifs de cubage

class Regime(models.Model):
    Nom = models.CharField(max_length=100, blank=True, null=True)
    

    def __str__(self):
        return self.Nom
    class Meta:
        verbose_name="Regime"
        verbose_name_plural="Regimes"
        
class Essences(models.Model):
    Parcelle= models.ManyToManyField(Parcellaire)
    canton= models.ForeignKey(Canton, on_delete=models.DO_NOTHING,null=True )
    Regime= models.ForeignKey(Regime, on_delete=models.DO_NOTHING,null=True )
    Nom = models.CharField(max_length=100, blank=True, null=True)
    Description= models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.Nom} - {self.Regime.Nom} - {self.Description}-{self.canton.nom}'
    
    class Meta:
        verbose_name="Essence"
        verbose_name_plural="Essences"

class Essenceliège(Essences):
    Typeliège= models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        
        return f'{self.Nom}-{self.Typeliège}-{self.Regime.Nom}-{self.canton.nom} '
    
    class Meta:
        verbose_name="Essenceliège"
        verbose_name_plural="Essencelièges"

class TarifCubage(models.Model):
    Essence= models.ForeignKey(Essences, on_delete=models.DO_NOTHING,null=True )
    formule = models.CharField(max_length=100, blank=True, null=True)
    typeVolume = models.CharField(max_length=100, blank=True, null=True)
    UniteMesure = models.CharField(max_length=100, blank=True, null=True)
    circonference_min = models.IntegerField(blank=True, null=True)
    circonference_max = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.formule} - {self.Essence.Nom}- {self.Essence.Regime}-{self.Essence.canton.nom}'

    class Meta:
        verbose_name="Tarif de cubage"
        verbose_name_plural="Tarifs de cubage"
#models des operations

class TypeEchantillonage(models.Model):
    Nom = models.CharField(max_length=100, blank=True, null=True)
    Description= models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.Nom
    
    class Meta:
        verbose_name="Type d'échantillonage"
        verbose_name_plural="Types d'échantillonage"

class Operation_de_calcul(models.Model):
    Nom = models.CharField(max_length=100, blank=True, null=True)
    TarifCubage=models.ForeignKey(TarifCubage, on_delete=models.DO_NOTHING,null=True )
    TypeEchantillonage=models.ForeignKey(TypeEchantillonage, on_delete=models.DO_NOTHING,null=True )
    Surface_de_placette=models.IntegerField(blank=True, null=True)
    Nombre_de_strate=models.IntegerField(blank=True, null=True)
    superficie_peuplement=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    varience_moyenne=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    ecart_type_moyenn=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    erreur_type_relative=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_moyenne_peuplement_hectare=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_total_du_peuplent=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)

    def __str__(self):
        return self.Nom
    class Meta:
        verbose_name="Operation de calcul de volume bois "
        verbose_name_plural="Operations de calcul de volume bois"

class Strate(models.Model):
    numero=models.IntegerField(blank=True, null=True)
    Operation_de_calcul=models.ForeignKey(Operation_de_calcul,on_delete=models.CASCADE,null=True )
    Superficie_de_la_strate=models.DecimalField(blank=True, null=True,max_digits=12, decimal_places=3)
    nombre_placette=models.IntegerField(blank=True, null=True)
    volume_moyenne_strate=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_total_strate=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    ecart_type_strate=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    erreur_standard=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    intervalle_confience=models.CharField(max_length=100, blank=True, null=True)
    parcelle=models.IntegerField(blank=True, null=True)
    groupe=models.CharField(max_length=100, blank=True, null=True)

class Placette(models.Model):
    numero_placette=models.IntegerField(blank=True, null=True)
    Strate=models.ForeignKey(Strate,on_delete=models.CASCADE,null=True )
    volume_total=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_hectares=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    nombre_de_bois_total=models.IntegerField(blank=True, null=True)
    CHOICES = [
        ('Squelettique', 'Squelettique'),
        ('Peu profond', 'Peu profond'),
        ('Profond', 'Profond'),
    ]

    Profondeur_de_sol = models.CharField(max_length=100, choices=CHOICES, null=True, blank=True)




class liste_de_bois(models.Model):
    Placette=models.ForeignKey(Placette,on_delete=models.CASCADE,null=True )
    circonferance_1m30=models.IntegerField(blank=True, null=True)
    hauteur=models.IntegerField(blank=True, null=True)
    volume_individuel=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    nombre_de_bois_classe=models.IntegerField(blank=True, null=True)
    volume_total_classe=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)


class Operation_de_calcul_de_Rendement(models.Model):
    Nom = models.CharField(max_length=100, blank=True, null=True)
    tarif_rendement_liege_reproduction = models.ForeignKey(TarifCubage, related_name='operation_de_calcul_de_rendement_reproduction',on_delete=models.CASCADE, null=True)
    tarif_rendement_liege_male = models.ForeignKey(TarifCubage, related_name='operation_de_calcul_de_rendement_male',on_delete=models.CASCADE, null=True)
    superficie_peuplement=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_total_liege_de_reproduction=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_total_liege_de_male=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_total_de_liege=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    parcelle=models.IntegerField(blank=True, null=True)
    groupe=models.CharField(max_length=100, blank=True, null=True)
    Annee_de_demasclage=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.Nom
    
    class Meta:
        verbose_name="Operation de calcul de Rendement liège"
        verbose_name_plural=" Operations de calcul de Rendement liège "



class liste_liege_par_Circonference(models.Model):
    operation_de_calcul_de_Rendement=models.ForeignKey(Operation_de_calcul_de_Rendement,on_delete=models.CASCADE,null=True )
    circonferance_1m30=models.IntegerField(blank=True, null=True)
    volume_individuel_liege_de_reproduction=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_individuel_liege_male=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_individuel_hausse=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    nombre_de_liege_de_reproduction_classe=models.IntegerField(blank=True, null=True)
    nombre_de_liege_de_male_classe=models.IntegerField(blank=True, null=True)
    volume_total_liege_de_reproduction_classe=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)
    volume_total_liege_de_male_classe=models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=3)









