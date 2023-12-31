# dans ce fichier nous creons des models pour notre BD, les models
# sont assimilable aux tables ou feuille dans un fichier excel et le fichier excel est
# assimilable a la BD.
# Donc ici nous creons de tables qui ont des rubriques comme comme 
# dans toute table ou feuille en excel (nom, prix, etc.) qui nous renseigne
# sur les information que la feuille contient
from django.db import models

# Model Manager, qui gere les infos de tout les manager de l'application
class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    pseudo = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.pseudo

# Model Hospital, qui gere les infos des tout les hopitaux du projet
# Ce model a une relation avec Manager car chaque hopital doit avoir un
# manager citee comme createur
class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length = 255)
    creator = models.ForeignKey(Manager, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
        
# Model Doctor pour la gestion des medecins
# ce model a une relation avec Hospital et Manager

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    creator = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name


#Model Patient pour la gestion des patients
class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20) 
    address = models.TextField()
    date = models.DateField(auto_now_add=True)
    symptoms = models.TextField()
    medications = models.TextField()
    status = models.CharField(max_length=50)
    disease_history = models.TextField()
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.full_name

# ajoutons un Model pour les utilisateurs
class User(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

# Model pour la liste d'attente ou demande de consultations
class Attente(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name
