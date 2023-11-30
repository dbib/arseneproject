# Cet fichier gere la vue de notre application, ie les infos que contiennent nos pages html
# ici nous attribuons  les donnees au fichiers html specifique, ces donnees sont alors
# accessible dans les fichiers html.

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Manager

# gestion de la connexion ou login
def login(request):
    #Ici on recuperer les infos ou donnees contenus dans la page login apres
    # que l'utilisateur est cliquer sur envoyer. Donnees qui sont dans la request
    # on check alors si il s'agit de la requette envoie (POST) pour recuperer les donnees
    # et les analysees
    if request.method == 'POST':
        pseudo = request.POST['pseudo']
        password = request.POST['password']
        
        # apres avoir recuperer les donnes et les placees dans nos variables
        # on check si ces donnees existent dans notre table ou feuille Manager
        try:
            manager = Manager.objects.get(pseudo=pseudo, password=password)
            # Si les donnees exist ie le manager exist on le redirect vers la page
            # manager_dashboard avec les donnees (ici manager_id)
            return redirect('manager_dashboard', manager_id=manager.id)
        except Manager.DoesNotExist:
            # si le manager n'existe pas, on envoie un message d'erreur
            messages.error(request, 'Pseudo ou password incorrect')
    
    return render(request, 'covidapp/login.html')
