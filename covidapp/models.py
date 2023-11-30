# dans ce fichier nous creons des models pour notre BD, les models
# sont assimilable aux tables ou feuille dans un fichier excel et le fichier excel est
# assimilable a la BD.
# Donc ici nous creons de tables qui ont des rubriques comme comme 
# dans toute table ou feuille en excel (nom, prix, etc.) qui nous renseigne
# sur les information que la feuille contient
from django.db import models

# Create your models here.
# Model Manager, qui gere les infos de tout les manager de l'application
class Managet(models.Model):
    id = models.AutoField(primary_key=True)
    pseudo = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.pseudo